from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..middleware import oauth2

from ..database.schemas import schemas

from ..database.models import models
from ..database.database import get_db
from ..middleware import utils


router = APIRouter(prefix = "/auth", tags = ["Authentication"])

@router.post("/login", status_code = status.HTTP_201_CREATED, response_model = schemas.Token,)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials")
    
    data = {"user_id": user.id}
    access_token = oauth2.create_acces_token(data)
   
    return {"access_token": access_token, "token_type": "bearer"}