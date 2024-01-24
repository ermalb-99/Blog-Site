from fastapi import FastAPI
import models
from database import engine
import blogs
import admin
import auth
import users

app = FastAPI(
    title='Blog Site',
    description='Where People Can Link Up'
)
app.include_router(router=blogs.router)
app.include_router(router=users.router)
app.include_router(router=auth.router)
app.include_router(router=admin.router)

models.Base.metadata.create_all(bind=engine)