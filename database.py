import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
from models import *
import models 

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    # This looks at all classes that inherited SQLModel and creates them in Postgres
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session