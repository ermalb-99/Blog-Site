from fastapi import APIRouter,Depends,HTTPException,status
from pydantic import BaseModel
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import UserModel,Users
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt , JWTError
from datetime import datetime ,timedelta

class Token(BaseModel):
    access_token : str 
    token_type : str 



router = APIRouter(
    tags=['Authentication / Auth'],
    prefix='/auth'
)


def get_db():
    db = SessionLocal()
    try : 
        yield db 
    finally:
        db.close()
db = Annotated[Session,Depends(get_db)]
bcrypt = CryptContext(schemes=['bcrypt'],deprecated='auto')
form = Annotated[OAuth2PasswordRequestForm,Depends()]
SECRET_KEY = 'b986fec08eba6be91aa6d140e3ba38eb2efdeb651e19b66f4e800a09fafd058b'
ALGORITHM = 'HS256'
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def authenticate_user(username:str,password:str,db:db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False 
    if not bcrypt.verify(password,user.password):
        return False 
    return user 

def create_access_token(username:str,user_id:int,role:str,expires_delta:timedelta):
    payload = {'sub':username , 'id':user_id,'role':role}
    expires = datetime.utcnow() + expires_delta
    payload.update({'exp':expires})
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        user_role : str = payload.get('role')
        if username is None or user_id is None :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could Not Validate")
        return {'username':username,'id':user_id,'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)




@router.post('/signup',summary='Sign up an User in Database')
async def signup_user(db:db,new:UserModel):
    new = Users(
        email = new.email.lower(),
        username = new.username.lower(),
        first_name = new.first_name.capitalize(),
        last_name = new.last_name.capitalize(),
        password = bcrypt.hash(new.password),
        role = new.role
    )
    db.add(new)
    db.commit()



@router.post('/token',response_model=Token,summary='Log In Form')
async def log_in_for_access(db:db,form:form):
    user = authenticate_user(form.username,form.password,db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = create_access_token(user.username,user.id,user.role,timedelta(minutes=20))
    return {'access_token':token,'token_type':'bearer'}

@router.get('/all')
async def read_all_users(db:db):
    return db.query(Users).all()