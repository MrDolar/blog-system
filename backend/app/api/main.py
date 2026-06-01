"""API Routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user, get_admin_user
from app.models.main_models import *

router = APIRouter(prefix="/api", tags=["Main"])

@router.get("/articles")
async def list_articles(page: int = 1, size: int = 10, category_id: int = None, db = Depends(get_db)):
    query = db.query(Article).filter(Article.status == "published")
    if category_id: query = query.filter(Article.category_id == category_id)
    return {"total": query.count(), "items": query.order_by(Article.created_at.desc()).offset((page-1)*size).limit(size).all()}

@router.post("/articles", status_code=201)
async def create_article(title: str, content: str, user = Depends(get_current_user), db = Depends(get_db)):
    a = Article(title=title, content=content, author_id=user.id)
    db.add(a); db.commit(); db.refresh(a)
    return a

@router.get("/articles/{id}")
async def get_article(id: int, db = Depends(get_db)):
    a = db.query(Article).filter(Article.id == id).first()
    if not a: raise HTTPException(404)
    a.views += 1; db.commit()
    return a

@router.post("/articles/{id}/comments", status_code=201)
async def add_comment(id: int, content: str, user = Depends(get_current_user), db = Depends(get_db)):
    db.add(Comment(article_id=id, user_id=user.id, content=content))
    db.commit()
    return {"message": "commented"}
