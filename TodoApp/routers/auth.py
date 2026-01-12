from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import User
from database import get_db
from passlib.context import CryptContext
from jose import jwt


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = "cade615d2f0189947329a2dd14c54e2c02ed4088bc0c511cb1655c3de4f0c592"
ALGORITHM = "HS256"

db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.get("/login")
def login():
    return {"message": "Login endpoint"}

@router.post("/token")
def get_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     db: db_dependency):
    user = find_user(db, form_data.username, form_data.password)
    if not user:
        return {"error": "Invalid credentials"}
    return {"access_token": create_access_token(user.username, user.id, timedelta(minutes=15)), "token_type": "bearer"}


def find_user(db: db_dependency, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user
    

def create_access_token(user_name: str, user_id: int, expires_delta: timedelta):
    expire = datetime.now(timezone.utc) + expires_delta
    encode = {"sub": user_name, "id": user_id, "exp": expire}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise exception
    except:
        raise exception
    return {"username": username, "id": user_id}
