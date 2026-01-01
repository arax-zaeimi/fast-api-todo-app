from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import models
from models import TodoItem
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/todos")
def read_todos(db: db_dependency):
    todos = db.query(TodoItem).all()
    return todos