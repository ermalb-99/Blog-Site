from sqlalchemy import Column,String,Integer,ForeignKey
from pydantic import BaseModel
from database import Base 

class Blogs(Base):
    __tablename__ = 'blogs'
    id=Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(Integer,ForeignKey('users.id'))

class BlogsModel(BaseModel):
    title : str 
    content : str 
    
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True)
    username = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    friends = Column(Integer)
    role = Column(String)

class UserModel(BaseModel):
    email : str 
    username : str 
    first_name : str 
    last_name : str 
    password : str 
    role:str


