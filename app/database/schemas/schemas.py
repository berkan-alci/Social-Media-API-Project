from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: Optional[str] = None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
    
class Post(PostBase):
    id: int
    created_at: datetime
    user: UserResponse

    class Config:
        orm_mode = True
    
class PostResponse(BaseModel):
    Post: Post
    Likes: int

    class Config:
        orm_mode = True

class LikeBase(BaseModel):
    post_id: int
    dir: bool
    
class LikePost(LikeBase):
    pass

class LikeResponse(LikeBase):
    class Config:
        orm_mode = True
    

    