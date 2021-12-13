from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from ..database.schemas import schemas

from ..database.models import models
from ..middleware import utils
from ..database.database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix = "/users", tags = ["Users"])

@router.get("/", response_model = List[schemas.UserResponse])
def get_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Users not found!")
    
    return user

@router.get("/{id}", response_model = schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} not found!")
    
    return user

@router.post("/register", status_code = status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #Hash pwd
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

