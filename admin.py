from fastapi import APIRouter,Depends,HTTPException,status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Blogs,Users
from auth import get_current_user

router = APIRouter(
    tags=['Admin'],
    prefix='/admin'

)

def get_db():
    db = SessionLocal()
    try : 
        yield db 
    finally:
        db.close()
db = Annotated[Session,Depends(get_db)]
user_dependecy = Annotated[dict,Depends(get_current_user)]

@router.get('/all',summary='Returns All Users In Database')
async def read_all_users(db:db,user:user_dependecy):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    data =  db.query(Users).all()
    return {'Data':data}


@router.get('/all/blogs/',summary='Returns All Blogs In Database')
async def read_all_blogs(db:db,user:user_dependecy):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    data = db.query(Blogs).all()
    return {'Data':data}


@router.get('/user/by/name/',summary='Returns a User by Name')
async def get_user_by_username(user:user_dependecy,name:str,db:db):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    data = db.query(Users).filter(Users.username == name.lower()).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {'Data':data}

@router.get('/user/by/id/',summary='Returns a User by ID')
async def get_user_by_id(user:user_dependecy,id:int,db:db):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    data = db.query(Users).filter(Users.id == id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {'Data':data}