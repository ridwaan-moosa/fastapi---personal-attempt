from importlib.resources import contents
from logging import exception
from multiprocessing import synchronize
from pickle import TRUE
from pyexpat import model
from turtle import title
from typing import Optional, List
from urllib import response
from fastapi import Body, FastAPI, Response, HTTPException, Depends, APIRouter
import psycopg2
from pydantic import BaseModel
import psycopg2 #used to import database from postgres
from psycopg2.extras import RealDictCursor # used to import the tables and columns from the database
import time
from .. import models, schemas
from ..database import engine,SessionLocal,get_db
from sqlalchemy.orm import session
from passlib.context import CryptContext

router = APIRouter(
    #prefix="/posts"     #can be used instead of stating the path eg.("/post") on every function
    tags=['users']
)

#______hashing alogorithm to hide passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #tells program what encryption to use

#____________create new user
@router.post("/users", status_code=201 )
def create_users(user: schemas.usercreate, db: session = Depends(get_db)):
   
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = models.users(**user.dict())

    db.add(new_user) 
    db.commit() 
    db.refresh(new_user) 

    return {"Data": new_user}


#____get users using orm sqlalchemy
@router.get("/users/{id}")
def getpost(id: int  ,response: Response,db: session = Depends(get_db)):
    
    users = db.query(models.users).filter(models.users.id == id).first()
    if not users:
        raise HTTPException(status_code=404 , detail= "not found ") 

    return {"details": users}