from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from database import get_db
from models import EcoPlace
from uuid import uuid4

router = APIRouter()

class EcoPlaceModel(BaseModel):
    id: Optional[str] = None
    name: str
    location: str
    description: str
    class Config:
        orm_mode = True

def generate_id():
    return str(uuid4())

@router.get("/", response_model=List[EcoPlaceModel])
async def get_eco_places(db: Session = Depends(get_db)):
    places = db.query(EcoPlace).all()
    return places

@router.post("/", response_model=EcoPlaceModel)
async def create_eco_place(place: EcoPlaceModel, db: Session = Depends(get_db)):
    new_place = EcoPlace(
        id=generate_id(),
        name=place.name,
        location=place.location,
        description=place.description
    )
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place

@router.get("/{place_id}", response_model=EcoPlaceModel)
async def get_eco_place(place_id: str, db: Session = Depends(get_db)):
    place = db.query(EcoPlace).filter(EcoPlace.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Eco-place not found")
    return place

@router.put("/{place_id}", response_model=EcoPlaceModel)
async def update_eco_place(place_id: str, place: EcoPlaceModel, db: Session = Depends(get_db)):
    existing_place = db.query(EcoPlace).filter(EcoPlace.id == place_id).first()
    if not existing_place:
        raise HTTPException(status_code=404, detail="Eco-place not found")
    existing_place.name = place.name
    existing_place.location = place.location
    existing_place.description = place.description
    db.commit()
    db.refresh(existing_place)
    return existing_place

@router.delete("/{place_id}", response_model=EcoPlaceModel)
async def delete_eco_place(place_id: str, db: Session = Depends(get_db)):
    place = db.query(EcoPlace).filter(EcoPlace.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Eco-place not found")
    db.delete(place)
    db.commit()
    return place