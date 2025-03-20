from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Annotated
from sqlalchemy.orm import Session
from database import get_db
from models import User, UserRole
from uuid import uuid4

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Pydantic модели
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    admin_code: Optional[str] = None

class LoginData(BaseModel):
    username: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str

class UserResponse(BaseModel):
    name: str
    email: EmailStr
    role: str
    user_id: str
    class Config:
        orm_mode = True

# Вспомогательные функции
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

def verify_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Неверный токен")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        return {"email": user.email, "role": user.role, "name": user.name, "user_id": user.user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    return verify_token(token, db)

def generate_id():
    return str(uuid4())

# Эндпоинты
@router.post("/register", response_model=dict)
def register(user: UserRegister, db: Session = Depends(get_db)):
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Пароль должен содержать минимум 6 символов")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже зарегистрирован")
    
    if user.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Роль должна быть 'admin' или 'user'")
    
    if user.role == "admin" and user.admin_code != "ECO_ADMIN_2025":
        raise HTTPException(status_code=403, detail="Неверный код администратора")
    
    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=UserRole.ADMIN if user.role == "admin" else UserRole.USER,
        user_id=generate_id()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Регистрация успешна", "user_id": new_user.user_id}

@router.post("/login", response_model=Token)
async def login(form_data: LoginData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    refresh_token = create_refresh_token(data={"sub": user.email, "role": user.role})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.user_id
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return current_user