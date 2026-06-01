from datetime import datetime
from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey
from app.core.database import Base

class Post(Base):
    __tablename__="posts"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(200),nullable=False,index=True)
    content=Column(Text,nullable=False)
    summary=Column(String(500),default="")
    author_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    category=Column(String(50),default="")
    tags=Column(String(200),default="")
    status=Column(String(20),default="draft")
    views=Column(Integer,default=0)
    created_at=Column(DateTime,default=datetime.utcnow)

class Comment(Base):
    __tablename__="comments"
    id=Column(Integer,primary_key=True,index=True)
    post_id=Column(Integer,ForeignKey("posts.id"),nullable=False)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    content=Column(Text,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)
