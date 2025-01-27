from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

users = []

@app.post("/users", response_model=User)
def create_user(user: User):
    if any(existing_user.id == user.id for existing_user in users):
        raise HTTPException(status_code=400, detail="User with this ID already exists")
    users.append(user)
    return user

@app.get("/users", response_model=List[User])
def get_users():
    return users

@app.get("/users/{id}", response_model=User)
def get_user(id: int):
    for user in users:
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{id}", response_model=User)
def update_user(id: int, updated_user: User):
    for index, user in enumerate(users):
        if user.id == id:
            users[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{id}", response_model=dict)
def delete_user(id: int):
    for index, user in enumerate(users):
        if user.id == id:
            users.pop(index)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
