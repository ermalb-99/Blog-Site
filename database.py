from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'sqlite:///./blog_database.db'
engine = create_engine(DATABASE_URL,connect_args={'check_same_thread':False})
Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)