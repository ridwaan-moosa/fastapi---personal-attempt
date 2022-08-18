from importlib.resources import contents
from logging import exception
from multiprocessing import synchronize
from pickle import TRUE
from pyexpat import model
from turtle import title
from typing import Optional, List
from urllib import response
from fastapi import Body, FastAPI, Response, HTTPException, Depends
import psycopg2
from pydantic import BaseModel
import psycopg2 #used to import database from postgres
from psycopg2.extras import RealDictCursor # used to import the tables and columns from the database
import time
from . import models,schemas
from app import models,schemas
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import session
from passlib.context import CryptContext
from .routers import post,users, auth, votes #import the new files
from . config import settings
from fastapi.middleware.cors import CORSMiddleware


#______create tables in models file ORM
models.Base.metadata.create_all(bind=engine) #creates all the tables from the "models" file

origins = ["*"] #put the webapp domain that is allowed to acecess your api < * is for all websites\
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router) #reference the new files the functions are saved in 
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)



