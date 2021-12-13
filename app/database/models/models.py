from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True,  nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key = True, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE", onupdate = "CASCADE"), nullable=False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'True', nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), server_default = text('now()'), nullable = False)
    
    user = relationship("User")
    
class Like(Base):
    __tablename__ = 'likes'
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE", onupdate = "CASCADE"), primary_key= True, nullable = False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete = "CASCADE", onupdate = "CASCADE"), primary_key = True, nullable = False)