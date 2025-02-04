from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4  

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 7

users = {}  
used_refresh_tokens = {}  
active_refresh_tokens = {}  

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    name: str
    email: EmailStr
    role: str
    user_id: str  

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None or email not in users:
            raise HTTPException(status_code=401, detail="Invalid token or user")
        return users[email]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/auth/register")
def register(user: UserRegister):
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Пароль должен содержать минимум 6 символов")
    
    if user.email in users:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже зарегистрирован")
    
    if user.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Роль должна быть 'admin' или 'user'")
    
    user_id = str(uuid4())
    
    hashed_password = hash_password(user.password)
    users[user.email] = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "role": user.role,
        "user_id": user_id  
    }
    return {"message": "Регистрация успешна", "user_id": user_id}

@app.post("/auth/login", response_model=Token)
def login(user: UserLogin):
    if user.email not in users:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    stored_user = users[user.email]
    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    access_token = create_access_token(data={"sub": user.email, "role": stored_user["role"]})
    refresh_token = create_refresh_token(data={"sub": user.email, "role": stored_user["role"]})
    
    if user.email in active_refresh_tokens:
        old_refresh_token = active_refresh_tokens[user.email]
        used_refresh_tokens[old_refresh_token] = datetime.utcnow()  
        print(f"Old refresh token {old_refresh_token} is now invalid.")
    
    active_refresh_tokens[user.email] = refresh_token

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@app.post("/auth/refresh", response_model=Token)
def refresh_token(refresh_token: str):
    if refresh_token in used_refresh_tokens:
        raise HTTPException(status_code=401, detail="Этот refresh token уже использован.")
    
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None or email not in users:
            raise HTTPException(status_code=401, detail="Invalid token or user")
        
        if datetime.utcnow() > datetime.utcfromtimestamp(payload["exp"]):
            raise HTTPException(status_code=401, detail="Refresh token has expired")

        used_refresh_tokens[refresh_token] = datetime.utcnow()

        new_access_token = create_access_token(data={"sub": email, "role": users[email]["role"]})
        new_refresh_token = create_refresh_token(data={"sub": email, "role": users[email]["role"]})
        
        active_refresh_tokens[email] = new_refresh_token
        
        return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@app.get("/auth/users")
def get_users():
    if not users:
        raise HTTPException(status_code=404, detail="Нет зарегистрированных пользователей")
    return {"registered_users": [{"email": email, "name": data["name"], "role": data["role"], "user_id": data["user_id"]} for email, data in users.items()]}

@app.get("/admin")
def admin(token: str = Depends(verify_token)):
    if token["role"] != "admin":
        raise HTTPException(status_code=403, detail="Нет доступа, требуется роль администратора")
    return {"message": f"Hello, {token['name']}! You have admin access."}

@app.get("/user-check")
def user_check(token: str = Depends(verify_token)):
    if token["role"] != "user":
        raise HTTPException(status_code=403, detail="Нет доступа, требуется роль пользователя")
    return {"message": f"Hello, {token['name']}! You have user access."}

@app.get("/me")
def me(token: str = Depends(verify_token)):
    return {"name": token["name"], "email": token["email"], "role": token["role"], "user_id": token["user_id"]}
