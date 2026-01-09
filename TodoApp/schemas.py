from typing import Optional
from pydantic import BaseModel, Field


class TodoItemRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = None
    priority: int = Field(default=1, ge=1, le=5)
    completed: bool = False

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, Bread, Eggs",
                "completed": False
            }
        }
    }

class UserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$')
    password: str = Field(min_length=6)
    first_name: str
    last_name: str
    role: Optional[str] = "user"


    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "strongpassword",
                "first_name": "John",
                "last_name": "Doe",
                "role": "user"
            }
        }
    }