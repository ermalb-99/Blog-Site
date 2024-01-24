from fastapi import APIRouter,Depends,HTTPException,status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Blogs,Users
from auth import get_current_user

router = APIRouter(
    tags=['Users'],
    prefix='/user'

)

def get_db():
    db = SessionLocal()
    try : 
        yield db 
    finally:
        db.close()
db = Annotated[Session,Depends(get_db)]
user_dependecy = Annotated[dict,Depends(get_current_user)]






@router.get('/my/blogs/',summary='Gets all Todos')
async def read_my_blogs(db:db,user:user_dependecy):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    data = db.query(Blogs).filter(Blogs.owner_id == user.get('id')).all()
    return data



@router.get('/my/info',status_code=status.HTTP_200_OK,summary='Info About User')
async def my_profile(db:db,user:user_dependecy):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    data = db.query(Users).filter(Users.id == user.get('id')).all()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return data 

@router.delete('/delete/myblog/{id}',status_code=status.HTTP_410_GONE,description="Blog Deleted",summary='Deletes a blog by id')
async def delete_my_blog_by_id(db:db,id:int,user:user_dependecy):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db.delete(db.query(Blogs).filter(Blogs.owner_id == user.get('user_id')).filter(Blogs.id == id).first())
    db.commit()


    
    
    
