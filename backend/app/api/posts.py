from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.post import Post,Comment

router=APIRouter(prefix="/api/posts",tags=["Posts"])

class PostCreate(BaseModel):
    title:str;content:str;summary:str="";category:str="";tags:str="";status:str="draft"

class CommentCreate(BaseModel):
    content:str

@router.get("")
async def list_posts(page:int=1,size:int=10,category:Optional[str]=None,keyword:Optional[str]=None,db:Session=Depends(get_db)):
    q=db.query(Post).filter(Post.status=="published")
    if category:q=q.filter(Post.category==category)
    if keyword:q=q.filter(Post.title.contains(keyword))
    return {"total":q.count(),"items":[{"id":p.id,"title":p.title,"summary":p.summary,"category":p.category,"views":p.views} for p in q.order_by(Post.created_at.desc()).offset((page-1)*size).limit(size).all()]}

@router.post("")
async def create_post(req:PostCreate,user=Depends(get_current_user),db:Session=Depends(get_db)):
    p=Post(**req.dict(),author_id=user.id);db.add(p);db.commit();db.refresh(p);return {"id":p.id,"title":p.title}

@router.get("/{pid}")
async def get_post(pid:int,db:Session=Depends(get_db)):
    p=db.query(Post).filter(Post.id==pid).first()
    if not p:raise HTTPException(404,"Not found")
    p.views+=1;db.commit()
    return {"id":p.id,"title":p.title,"content":p.content,"summary":p.summary,"category":p.category,"tags":p.tags,"views":p.views}

@router.delete("/{pid}")
async def delete_post(pid:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    p=db.query(Post).filter(Post.id==pid,Post.author_id==user.id).first()
    if not p:raise HTTPException(404,"Not found")
    db.delete(p);db.commit();return {"message":"Deleted"}

@router.post("/{pid}/comments")
async def add_comment(pid:int,req:CommentCreate,user=Depends(get_current_user),db:Session=Depends(get_db)):
    db.add(Comment(post_id=pid,user_id=user.id,content=req.content));db.commit();return {"message":"Comment added"}

@router.get("/{pid}/comments")
async def list_comments(pid:int,db:Session=Depends(get_db)):
    return {"items":[{"id":c.id,"content":c.content,"user_id":c.user_id} for c in db.query(Comment).filter(Comment.post_id==pid).all()]}
