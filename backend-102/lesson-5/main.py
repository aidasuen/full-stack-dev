from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

users = {}

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/auth/register")
def register(user: UserRegister):
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Пароль должен содержать минимум 6 символов")
    
    if user.email in users:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже зарегистрирован")
    
    hashed_password = hash_password(user.password)
    users[user.email] = {"name": user.name, "email": user.email, "password": hashed_password}
    return {"message": "Регистрация успешна"}

@app.post("/auth/login")
def login(user: UserLogin):
    if user.email not in users:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    stored_user = users[user.email]
    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    return {"message": "Успешный вход", "user": {"name": stored_user["name"], "email": stored_user["email"]}}

@app.get("/auth/users")
def get_users():
    if not users:
        raise HTTPException(status_code=404, detail="Нет зарегистрированных пользователей")
    return {"registered_users": [{"email": email, "name": data["name"]} for email, data in users.items()]}
