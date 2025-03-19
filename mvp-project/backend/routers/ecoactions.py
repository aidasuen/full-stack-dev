from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from database import get_db
from models import EcoAction, EcoActionType
from uuid import uuid4

router = APIRouter()

class EcoActionModel(BaseModel):
    id: Optional[str] = None
    location: str
    action_type: str
    description: str
    class Config:
        orm_mode = True

def generate_id():
    return str(uuid4())

@router.get("/", response_model=List[EcoActionModel])
async def get_eco_actions(db: Session = Depends(get_db)):
    actions = db.query(EcoAction).all()
    return actions

@router.post("/", response_model=EcoActionModel)
async def create_eco_action(action: EcoActionModel, db: Session = Depends(get_db)):
    if action.action_type not in EcoActionType.__members__:
        raise HTTPException(status_code=400, detail="Неверный тип действия")
    new_action = EcoAction(
        id=generate_id(),
        location=action.location,
        action_type=EcoActionType[action.action_type.upper()],
        description=action.description
    )
    db.add(new_action)
    db.commit()
    db.refresh(new_action)
    return new_action

@router.get("/{action_id}", response_model=EcoActionModel)
async def get_eco_action(action_id: str, db: Session = Depends(get_db)):
    action = db.query(EcoAction).filter(EcoAction.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Eco action not found")
    return action

@router.put("/{action_id}", response_model=EcoActionModel)
async def update_eco_action(action_id: str, action: EcoActionModel, db: Session = Depends(get_db)):
    existing_action = db.query(EcoAction).filter(EcoAction.id == action_id).first()
    if not existing_action:
        raise HTTPException(status_code=404, detail="Eco action not found")
    if action.action_type not in EcoActionType.__members__:
        raise HTTPException(status_code=400, detail="Неверный тип действия")
    existing_action.location = action.location
    existing_action.action_type = EcoActionType[action.action_type.upper()]
    existing_action.description = action.description
    db.commit()
    db.refresh(existing_action)
    return existing_action

@router.delete("/{action_id}", response_model=EcoActionModel)
async def delete_eco_action(action_id: str, db: Session = Depends(get_db)):
    action = db.query(EcoAction).filter(EcoAction.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Eco action not found")
    db.delete(action)
    db.commit()
    return action