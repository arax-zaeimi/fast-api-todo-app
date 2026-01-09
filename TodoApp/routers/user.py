from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserRequest
from models import User
from passlib.context import CryptContext

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/user")
def create_user(db: db_dependency, user_request: UserRequest):
    
    existing_user = db.query(User).filter(
        (User.username == user_request.username) |
        (User.email == user_request.email)
        ).first()
    if existing_user:
        return {"error": "Username already exists"}
    
    user_model = User(
        username=user_request.username,
        email=user_request.email,
        hashed_password=bcrypt_context.hash(user_request.password),
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        role=user_request.role
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model