from sqlmodel import SQLModel, create_engine, Session
from ..models.db_models import * 

DATABASE_URL = "postgresql://username:password@localhost:5432/mydatabase"

# engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    # SQLModel.metadata.create_all(engine)
    pass

def get_session():
    # return Session(engine)
    pass