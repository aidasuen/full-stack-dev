from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Секретный ключ и алгоритм для генерации JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    name: str
    email: EmailStr

# Заглушка базы данных пользователей
users = {}

# Хеширование пароля с использованием bcrypt
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Функция для создания JWT токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Функция для валидации JWT токена
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None or email not in users:
            raise HTTPException(status_code=401, detail="Invalid token or user")
        return users[email]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Регистрация нового пользователя
@app.post("/auth/register")
def register(user: UserRegister):
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Пароль должен содержать минимум 6 символов")
    
    if user.email in users:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже зарегистрирован")
    
    hashed_password = hash_password(user.password)
    users[user.email] = {"name": user.name, "email": user.email, "password": hashed_password}
    return {"message": "Регистрация успешна"}

# Вход пользователя с получением JWT токена
@app.post("/auth/login")
def login(user: UserLogin):
    if user.email not in users:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    stored_user = users[user.email]
    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Получение всех зарегистрированных пользователей (без токена)
@app.get("/auth/users")
def get_users():
    if not users:
        raise HTTPException(status_code=404, detail="Нет зарегистрированных пользователей")
    return {"registered_users": [{"email": email, "name": data["name"]} for email, data in users.items()]}

# Защищённый эндпоинт
@app.get("/protected")
def protected(token: str = Depends(verify_token)):
    return {"message": f"Hello, {token['name']}! This is a protected route."}

# Получение информации о текущем пользователе
@app.get("/me")
def me(token: str = Depends(verify_token)):
    return {"name": token["name"], "email": token["email"]}
