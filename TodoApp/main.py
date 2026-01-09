from fastapi import FastAPI
from routers import auth, todo, user
import models
from database import engine

app = FastAPI()
app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(user.router)

models.Base.metadata.create_all(bind=engine)