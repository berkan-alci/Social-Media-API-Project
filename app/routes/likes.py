from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database.schemas import schemas
from ..database.models import models
from ..middleware import oauth2
from ..database.database import engine, get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix ="/likes", tags= ["Likes"])

@router.get("/")
def get_likes():
    pass

@router.post("/", status_code = status.HTTP_201_CREATED)
def post_likes(like: schemas.LikePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    dir: bool = bool(like.dict().get('dir'))
    post_id: int = int(like.dict().get('post_id'))
    
    like_query = db.query(models.Like).filter(models.Like.post_id == post_id, models.Like.user_id == current_user.id)
    like = like_query.first()
    
    if dir:
        if like:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"user {current_user.id} has already liked the post {post_id}" )
        new_like = models.Like(post_id = post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        
        return Response(status_code = status.HTTP_202_ACCEPTED)
    else:
        if not like:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Like does not exist!")
        
        like_query.delete(synchronize_session = False)
        db.commit()
        return Response(status_code = status.HTTP_202_ACCEPTED)
        
