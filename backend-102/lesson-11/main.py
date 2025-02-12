from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List
from uuid import uuid4
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

# Настройки для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Настройки для JWT
SECRET_KEY = "your_secret_key"  # Замените на свой секретный ключ
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Хранилище данных
users = {}  # Словарь для хранения пользователей (ключ — email)
used_refresh_tokens = {}  # Словарь для использованных refresh токенов
active_refresh_tokens = {}  # Словарь для активных refresh токенов
places = []  # Список для хранения мест

# Схема для OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Модели Pydantic
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

class Place(BaseModel):
    name: str
    description: str
    location: str
    id: Optional[int] = None  # Поле id не обязательно и будет генерироваться сервером

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

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None or email not in users:
            raise HTTPException(status_code=401, detail="Неверный токен или пользователь")
        return users[email]
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)  # Проверка и получение пользователя

# Эндпоинты
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
    
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "role": user.role,
        "user_id": user_id  
    }
    
    users[user.email] = new_user
    return {"message": "Регистрация успешна", "user_id": user_id}

@app.post("/auth/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = next((u for u in users.values() if u["email"] == form_data.username), None)
    
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    
    access_token = create_access_token(data={"sub": user["email"], "role": user["role"]})
    refresh_token = create_refresh_token(data={"sub": user["email"], "role": user["role"]})
    
    if user["email"] in active_refresh_tokens:
        old_refresh_token = active_refresh_tokens[user["email"]]
        used_refresh_tokens[old_refresh_token] = datetime.utcnow()
    
    active_refresh_tokens[user["email"]] = refresh_token
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@app.post("/auth/refresh")
def refresh_token(refresh_token: str):
    if refresh_token in used_refresh_tokens:
        raise HTTPException(status_code=401, detail="Этот refresh токен уже использован.")
    
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None or email not in users:
            raise HTTPException(status_code=401, detail="Неверный токен или пользователь")
        
        if datetime.utcnow() > datetime.utcfromtimestamp(payload["exp"]):
            raise HTTPException(status_code=401, detail="Срок действия refresh токена истек")
        
        used_refresh_tokens[refresh_token] = datetime.utcnow()
        
        new_access_token = create_access_token(data={"sub": email, "role": users[email]["role"]})
        new_refresh_token = create_refresh_token(data={"sub": email, "role": users[email]["role"]})
        
        active_refresh_tokens[email] = new_refresh_token
        
        return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный refresh токен")

@app.get("/auth/users")
def get_users():
    if not users:
        raise HTTPException(status_code=404, detail="Нет зарегистрированных пользователей")
    return {"registered_users": [{"email": email, "name": data["name"], "role": data["role"], "user_id": data["user_id"]} for email, data in users.items()]}

@app.get("/admin")
def admin(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Нет доступа, требуется роль администратора")
    return {"message": f"Hello, {user['name']}! You have admin access."}

@app.get("/user-check")
def user_check(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if user["role"] != "user":
        raise HTTPException(status_code=403, detail="Нет доступа, требуется роль пользователя")
    return {"message": f"Hello, {user['name']}! You have user access."}

@app.get("/me")
def me(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    return {"name": user["name"], "email": user["email"], "role": user["role"], "user_id": user["user_id"]}

@app.post("/auth/logout")
def logout_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = verify_token(token)
    email = user["email"]
    
    if email not in active_refresh_tokens:
        raise HTTPException(status_code=401, detail="Нет активной сессии для выхода")
    
    del active_refresh_tokens[email]
    return {"message": "Выход выполнен успешно"}

@app.post("/places", response_model=Place)
def create_place(place: Place, user: dict = Depends(get_current_user)):
    if not place.name or not place.description or not place.location:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Все поля должны быть заполнены")
    
    place_id = len(places) + 1  # Генерация уникального ID
    new_place = place.dict()  # Получаем данные из модели
    new_place["id"] = place_id  # Устанавливаем ID
    new_place["owner"] = user["email"]  # Присваиваем владельца
    places.append(new_place)
    return new_place

@app.get("/places", response_model=List[Place])
def list_places(user: dict = Depends(get_current_user)):
    user_places = [place for place in places if place["owner"] == user["email"]]
    return user_places

@app.get("/places/{place_id}", response_model=Place)
def get_place(place_id: int, user: dict = Depends(get_current_user)):
    place = next((place for place in places if place["id"] == place_id and place["owner"] == user["email"]), None)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place

@app.put("/places/{place_id}", response_model=Place)
def update_place(place_id: int, updated_place: Place, user: dict = Depends(get_current_user)):
    place = next((place for place in places if place["id"] == place_id and place["owner"] == user["email"]), None)
    if not place:
        raise HTTPException(status_code=404, detail="Место не найдено или нет права на изменение")
    
    place.update(updated_place.dict(exclude_unset=True))
    
    return place

@app.delete("/places/{place_id}")
def delete_place(place_id: int, user: dict = Depends(get_current_user)):
    global places
    place = next((place for place in places if place["id"] == place_id and place["owner"] == user["email"]), None)
    
    if not place:
        raise HTTPException(status_code=404, detail="Место не найдено или нет прав на удаление")
    
    # Вместо создания новой локальной переменной places, нужно обновить глобальный список
   
    places = [place for place in places if not (place["id"] == place_id and place["owner"] == user["email"])]
    
    return {"message": "Место удалено успешно"}


