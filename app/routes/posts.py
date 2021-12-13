from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from ..database.schemas import schemas

from ..database.models import models
from ..middleware import oauth2
from ..database.database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

router = APIRouter(prefix = "/posts", tags = ["Posts"])


#
@router.get("/", response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    

    post_query = db.query(models.Post, func.count(models.Like.post_id).label("Likes")).join(
        models.Like, models.Like.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip)

    posts = post_query.all()
   
    return posts

@router.get("/{id}", response_model = schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post, func.count(models.Like.post_id).label("Likes")).join(
        models.Like, models.Like.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first() 
    print
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    
    return post

@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
 
    new_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found!")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform requested action!")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code = status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found!")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform requested action!")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()


#Routes for individual users

@router.get("/user", response_model= List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    posts_query = db.query(models.Post).filter(models.Post.user_id == current_user.id)
    post = posts_query.first()
    posts = posts_query.all()
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform requested action!")
    
    return posts

@router.get("/user/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first() 
    print
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform requested action!")
    return post