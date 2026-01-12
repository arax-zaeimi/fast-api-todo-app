from typing import Annotated
from fastapi import Depends, HTTPException, Path, status, APIRouter
from sqlalchemy.orm import Session
from models import TodoItem
from database import get_db
from schemas import TodoItemRequest
from .auth import get_current_user

db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

@router.get("/")
def read_todos(db: db_dependency):
    todos = db.query(TodoItem).all()
    return todos

@router.get("/{id}")
def read_todo(db: db_dependency, id: int = Path(gt=0)):
    todo = db.query(TodoItem).filter(TodoItem.id == id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependency,
                user: current_user_dependency,
                createTodoRequest: TodoItemRequest):
    
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    todo_model = TodoItem(**createTodoRequest.model_dump(), owner_id=user["id"])
    db.add(todo_model)
    db.commit()    
    db.refresh(todo_model)
    return todo_model

@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: db_dependency, id: int, updateTodoRequest: TodoItemRequest):
    todo_model = db.query(TodoItem).filter(TodoItem.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    for key, value in updateTodoRequest.model_dump().items():
        setattr(todo_model, key, value)
    
    db.commit()
    return

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: db_dependency, id: int):
    todo_model = db.query(TodoItem).filter(TodoItem.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo_model)
    db.commit()
    return