from fastapi import FastAPI
from .database.models import models
from .database.database import engine
from .routes import posts, users, auth, likes
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"] 
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API"}







