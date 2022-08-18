from psycopg2.extras import RealDictCursor # used to import the tables and columns from the database
import psycopg2
from fastapi import Body, FastAPI, Response, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy import func 
from app import oauth2
from .. import models,schemas
from ..database import engine,SessionLocal,get_db
from sqlalchemy.orm import session
import time
from sqlalchemy.sql.functions import func

router = APIRouter(
    #prefix="/posts"     #can be used instead of stating the path eg.("/post") on every function
    tags=['post/apialchemy']
)



#_______ est connection to db without ORM
while True: #continuosly attempt to est connection
    try: #when setting up connections use try to be able to tell if a connection can be established 
        conn = psycopg2.connect(host= 'localhost',database= 'Fastapi',user= 'postgres',
        password= '0165562314',cursor_factory=RealDictCursor) #(hostname,database,user,password,cursor)
        cursor = conn.cursor() # method used to run sql statements 
        print("Connection is established")
        break #break out of the while lopp
    except Exception as error:
        print("unable to establish connection")
        print("error" ,error)
        time.sleep(5) #wait 5 sec to retry to est connection 







#________get all post using ORM sqlalchemy
@router.get("/sqlalchemy" )#response_model=schemas.postresp ensure info sent back is what we defined in the schemas file
def test_posts(db: session = Depends(get_db),limit: int = 3, skip: int=0, search: Optional[str] = ""): #limit,skip,search are filtering options for the get posts router
    posts = db.query(models.post).filter(models.post.tittle.contains(search)).limit(limit).offset(skip).all() #provides filtering options for the get post router
    results = db.query(models.post, func.count(models.vote.post_id).label("votes")).join(models.vote, models.vote.post_id == models.post.id, isouter=True).group_by(models.post.id).filter(models.post.tittle.contains(search)).limit(limit).offset(skip).all()
    return {"data": results}


#____get all posts using sql statements
@router.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"Data": posts}



#_____create post using sql statements
@router.post("/posts", status_code=201, response_model=schemas.PostBase)
def createpost(Post: schemas.postcreate):
    
    cursor.execute("""INSERT INTO posts (tittle,contents,published) VALUES (%s,%s,%s) RETURNING * """,
    (Post.tittle, Post.contents, Post.published))# %s can be used to pass variables in sql ,avoid using the variables directly this is prone to sql injection
    
    new_post = cursor.fetchone() #used to retrieve the RETURNING values
    
    conn.commit() #saves entry to the database
   
    return {"Data": new_post}



#_____Create a posts using ORM (sqlalchemy)
@router.post("/sqlalchemy", status_code=201)
def createpost(post: schemas.postcreate,db: session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #<--must enter db: session = Depends(get_db) here becoz its a dependency #get_current_user makes sure user is logged in or has token befor they can create post
    new_post = models.post( **post.dict())#store new values #u can use the dict() to unpack the variable in a post instead of doing one by one 
    
    db.add(new_post) #add new post to db
    db.commit() #save it to db
    db.refresh(new_post) #return values of the new post

    return {"Data": new_post}



#____get specific post using sql
@router.get("/posts/{id}")
def getpost(id: int  ,response: Response): #id: int(error handling to ensure an int is used)
    cursor.execute("""SELECT * FROM posts WHERE id= %s """,(str(id)))
    post = cursor.fetchone()



#____get specific post using ORM
@router.get("/sqlalchemy/{id}")
def getpost(id: int  ,response: Response,db: session = Depends(get_db)):
    
    post = db.query(models.post, func.count(models.vote.post_id).label("votes")).join(models.vote, models.vote.post_id == models.post.id, isouter=True).group_by(models.post.id).filter(models.post.id == id).first()
    if not post:
        raise HTTPException(status_code=404 , detail= "not found ") 

    return {"details": post}




#_______delete post using sql
@router.delete("/posts/{id}")
def deletepost(id: int, get_current_user: int = Depends(oauth2.get_current_user)):
    
    cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""",(str(id)))
    del_post = cursor.fetchone()

    if del_post == None:
        raise HTTPException(status_code=404 , detail= "entry does not exsist")
    
    
    conn.commit()
    return{"message":"this post is deleted"}




#_______delete post using ORM
@router.delete("/sqlalchemy/{id}")
def deletepost(id: int, db: session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.post).filter(models.post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=404 , detail= "entry does not exsist")
    
    #if post.owner_id != oauth2.get_current_user.id :
      #  raise HTTPException(status_code=403 , detail="unauthorized to complete action")

    post.delete(synchronize_session=False)
    db.commit()

    return{"message":"this post is deleted"}




#_____update posts using sql
@router.put("/posts/{id}")
def putpost(id: int, post: schemas.postcreate, get_current_user: int = Depends(oauth2.get_current_user)):
        
    cursor.execute("""UPDATE posts SET tittle= %s ,contents= %s,published= %s WHERE id=%s RETURNING * """,
    (post.tittle,post.contents,post.published,str(id)))
    up_post = cursor.fetchone()
    conn.commit()

    if up_post == None:
        raise HTTPException(status_code=404 , detail= "post not found")
    
    
    return {"update": up_post}



#_____update posts using ORM
@router.put("/sqlalchemy/{id}")
def putpost(id: int, up_post: schemas.postcreate,db: session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    
    post_q = db.query(models.post).filter(models.post.id == id)
    post = post_q.first()
    
    if  post == None:
        raise HTTPException(status_code=404 , detail= "post not found")
    
    post_q.update(up_post.dict(), synchronize_session=False)
    db.commit()

    #if post.owner_id != oauth2.get_current_user.id :
      #  raise HTTPException(status_code=403 , detail="unauthorized to complete action")

    return {"update": post_q.first()}