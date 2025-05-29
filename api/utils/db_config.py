from sqlmodel import SQLModel, create_engine, Session
from models.db_models import * 
from dotenv import load_dotenv
import os
load_dotenv() 

DATABASE_URL = os.getenv("POSTGRES")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    # pass

def get_session():
    return Session(engine)
    # pass
def get_db_url(): 
    return DATABASE_URL