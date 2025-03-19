from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from models import User
from routers.auth import get_current_user, UserResponse

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    include_in_schema=False  
)

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Только администраторы могут просматривать список пользователей")
    users = db.query(User).all()
    return users

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Только администраторы могут удалять пользователей")
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if user.user_id == current_user["user_id"]:
        raise HTTPException(status_code=400, detail="Нельзя удалить самого себя")
    db.delete(user)
    db.commit()
    return {"message": "Пользователь удалён"}