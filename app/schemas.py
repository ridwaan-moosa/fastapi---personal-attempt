from distutils.util import convert_path
from operator import le
from typing import Union
from pydantic import BaseModel,EmailStr


class PostBase(BaseModel): #schemas from the pydantic model/ define the layout of the post
    tittle: str
    contents: str
    published: bool = True
    owner_id: int

class postcreate(PostBase):
    #owner_id: int
    pass

class postresp(PostBase): #response schema ensures user dont recieve unnecassary info or important info
    

    class config:   #copy&paste code to ensure response model doesnt give a error
        orm_mode = True

class usercreate(BaseModel):
    email: EmailStr
    password: str

class usersout(BaseModel):
    #id: int
    email: EmailStr

    class config:   #copy&paste code to ensure response model doesnt give a error
        orm_mode = True

class userlogin(BaseModel):
    email: EmailStr
    password: str

class token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):

    username: Union[str, None] = None

class Vote(BaseModel):
    post_id: int
    dir: int


