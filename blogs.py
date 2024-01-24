from fastapi import APIRouter,Depends,HTTPException,status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Blogs,BlogsModel
from auth import get_current_user

router = APIRouter(
    tags=['Blogs API'],
    prefix='/blog'
)

def get_db():
    db = SessionLocal()
    try : 
        yield db 
    finally:
        db.close()
db = Annotated[Session,Depends(get_db)]
user_dependecy = Annotated[dict,Depends(get_current_user)]

@router.get('/blogs')
async def blog(user:user_dependecy):
    return 'Blogs'

@router.post('/post/new/blog')
async def post_new_blog(new:BlogsModel,db:db,user:user_dependecy):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    new = Blogs(**new.model_dump(),owner_id = user.get('id'))
    db.add(new)
    db.commit()

@router.put('/update/blog/{blog_id}')
async def update_blog_by_id(db:db,
                            blog_id:int
                            ,user:user_dependecy,
                            new:BlogsModel
                            ):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    data = db.query(Blogs).filter(Blogs.id == blog_id).filter(Blogs.owner_id == user.get('id')).first()
    if not data :
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    data.title = new.title
    data.content = new.content
    db.add(data)
    db.commit()

@router.delete('/delete/blog/{id}')
async def delete_blog_by_id(db:db,id:int,user:user_dependecy):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    data = db.query(Blogs).filter(Blogs.id==id).first()
    if data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db.delete(data)
    db.commit()
