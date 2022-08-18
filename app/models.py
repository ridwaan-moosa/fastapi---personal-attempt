from cgitb import text
import email
from tkinter import CASCADE
from .database import Base
from sqlalchemy import TIMESTAMP, ForeignKey, PrimaryKeyConstraint, Column,String,Integer,Boolean, true
from sqlalchemy.sql.expression import null

class post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True , nullable=False) #specify the constraints of the table
    tittle = Column(String, nullable=False)
    contents = Column(String, nullable=False)
    published = Column(Boolean, server_default='True',nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False )

    class config:   #copy&paste code to ensure response model doesnt give a error
        orm_mode = True


class users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True , nullable=False) #specify the constraints of the table
    email = Column(String, nullable=False, unique=True)
    password = Column(String,nullable=False )

class vote(Base):
    __tablename__ = "votes"

    post_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),primary_key=True ,nullable=False)
    user_id = Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True ,nullable=False)