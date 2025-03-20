from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from database import get_db
from models import Reward
from uuid import uuid4

router = APIRouter()

class RewardModel(BaseModel):
    id: Optional[str] = None
    name: str
    points_needed: int
    description: str
    class Config:
        orm_mode = True

def generate_id():
    return str(uuid4())

@router.get("/", response_model=List[RewardModel])
async def get_eco_rewards(db: Session = Depends(get_db)):
    rewards = db.query(Reward).all()
    return rewards

@router.post("/", response_model=RewardModel)
async def create_eco_reward(reward: RewardModel, db: Session = Depends(get_db)):
    new_reward = Reward(
        id=generate_id(),
        name=reward.name,
        points_needed=reward.points_needed,
        description=reward.description
    )
    db.add(new_reward)
    db.commit()
    db.refresh(new_reward)
    return new_reward

@router.get("/{reward_id}", response_model=RewardModel)
async def get_eco_reward(reward_id: str, db: Session = Depends(get_db)):
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    return reward

@router.put("/{reward_id}", response_model=RewardModel)
async def update_eco_reward(reward_id: str, reward: RewardModel, db: Session = Depends(get_db)):
    existing_reward = db.query(Reward).filter(Reward.id == reward_id).first()
    if not existing_reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    existing_reward.name = reward.name
    existing_reward.points_needed = reward.points_needed
    existing_reward.description = reward.description
    db.commit()
    db.refresh(existing_reward)
    return existing_reward

@router.delete("/{reward_id}", response_model=RewardModel)
async def delete_eco_reward(reward_id: str, db: Session = Depends(get_db)):
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    db.delete(reward)
    db.commit()
    return reward