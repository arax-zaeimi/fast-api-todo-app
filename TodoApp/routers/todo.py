from typing import Annotated
from fastapi import Depends, HTTPException, Path, status, APIRouter
from sqlalchemy.orm import Session
from models import TodoItem
from database import get_db
from schemas import TodoItemRequest

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter()



@router.get("/todos")
def read_todos(db: db_dependency):
    todos = db.query(TodoItem).all()
    return todos

@router.get("/todos/{id}")
def read_todo(db: db_dependency, id: int = Path(gt=0)):
    todo = db.query(TodoItem).filter(TodoItem.id == id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependency, createTodoRequest: TodoItemRequest):
    todo_model = TodoItem(**createTodoRequest.model_dump())
    db.add(todo_model)
    db.commit()    
    db.refresh(todo_model)
    return todo_model

@router.put("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: db_dependency, id: int, updateTodoRequest: TodoItemRequest):
    todo_model = db.query(TodoItem).filter(TodoItem.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    for key, value in updateTodoRequest.model_dump().items():
        setattr(todo_model, key, value)
    
    db.commit()
    return

@router.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: db_dependency, id: int):
    todo_model = db.query(TodoItem).filter(TodoItem.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo_model)
    db.commit()
    return