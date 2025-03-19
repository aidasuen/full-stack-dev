from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models import ForumPost
from routers.auth import get_current_user
from uuid import uuid4

router = APIRouter()

class ForumPostModel(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    user_email: str
    timestamp: datetime
    class Config:
        orm_mode = True

def generate_id():
    return str(uuid4())

@router.get("/", response_model=List[ForumPostModel])
async def get_forum_posts(db: Session = Depends(get_db)):
    posts = db.query(ForumPost).all()
    return posts

@router.post("/", response_model=ForumPostModel)
async def create_forum_post(post: ForumPostModel, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    new_post = ForumPost(
        id=generate_id(),
        title=post.title,
        content=post.content,
        user_email=current_user["email"],
        timestamp=datetime.utcnow()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{post_id}", response_model=ForumPostModel)
async def update_forum_post(post_id: str, post: ForumPostModel, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if existing_post.user_email != current_user["email"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Вы не можете редактировать чужой пост")
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.timestamp = datetime.utcnow()
    db.commit()
    db.refresh(existing_post)
    return existing_post

@router.delete("/{post_id}", response_model=ForumPostModel)
async def delete_forum_post(post_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_email != current_user["email"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Вы не можете удалить чужой пост")
    db.delete(post)
    db.commit()
    return post