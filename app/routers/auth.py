from fastapi import Body, FastAPI, Response, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import oauth2
from ..database import engine,SessionLocal,get_db
from sqlalchemy.orm import session
from .. import schemas,models
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #tells program what encryption to use

def verify(p_password , h_password):
    return pwd_context.verify(p_password,h_password)


@router.post("/login")
def login(user_cred: OAuth2PasswordRequestForm = Depends(),db: session = Depends(get_db)):
    user = db.query(models.users).filter(models.users.email == user_cred.username).first() #find the email in the database

    if not user:
        raise HTTPException(status_code=404 , detail=f"invalid credentials")
    
    if not verify(user_cred.password, user.password):
        raise HTTPException(status_code=404 , detail= f"invalid credentials")

    #create token 
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    #return token
    return {"access_token": access_token, "token_type":"bearer"}