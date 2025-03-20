from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from database import get_db
from models import Route
from uuid import uuid4

router = APIRouter()

class RouteModel(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    difficulty: str
    length_km: float
    eco_friendly: bool
    class Config:
        orm_mode = True

def generate_id():
    return str(uuid4())

@router.get("/environmental", response_model=List[RouteModel])
async def get_eco_routes(db: Session = Depends(get_db)):
    routes = db.query(Route).all()
    return routes

@router.post("/environmental", response_model=RouteModel)
async def create_eco_route(route: RouteModel, db: Session = Depends(get_db)):
    new_route = Route(
        id=generate_id(),
        name=route.name,
        description=route.description,
        difficulty=route.difficulty,
        length_km=route.length_km,
        eco_friendly=route.eco_friendly
    )
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route

@router.get("/environmental/{route_id}", response_model=RouteModel)
async def get_eco_route(route_id: str, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.put("/environmental/{route_id}", response_model=RouteModel)
async def update_eco_route(route_id: str, route: RouteModel, db: Session = Depends(get_db)):
    existing_route = db.query(Route).filter(Route.id == route_id).first()
    if not existing_route:
        raise HTTPException(status_code=404, detail="Route not found")
    existing_route.name = route.name
    existing_route.description = route.description
    existing_route.difficulty = route.difficulty
    existing_route.length_km = route.length_km
    existing_route.eco_friendly = route.eco_friendly
    db.commit()
    db.refresh(existing_route)
    return existing_route

@router.delete("/environmental/{route_id}", response_model=RouteModel)
async def delete_eco_route(route_id: str, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    db.delete(route)
    db.commit()
    return route