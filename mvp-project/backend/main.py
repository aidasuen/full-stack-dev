from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List
from uuid import uuid4
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 7


users = {}  
used_refresh_tokens = {} 
active_refresh_tokens = {}  
eco_routes = []
eco_places = []
eco_rewards = []
eco_actions = {
    "recycling": [],
    "reusable_stores": []
}
community_posts = []

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

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

class Route(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    difficulty: str  # например, "легкий", "средний", "сложный"
    length_km: float
    eco_friendly: bool

class EcoPlace(BaseModel):
    id: Optional[str] = None
    name: str
    location: str
    description: str

class Reward(BaseModel):
    id: Optional[str] = None
    name: str
    points_needed: int
    description: str

class EcoAction(BaseModel):
    id: Optional[str] = None
    location: str
    action_type: str  # например, "переработка", "магазин"
    description: str

class ForumPost(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    user_email: str  # email автора
    timestamp: datetime

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
    return verify_token(token)  

def generate_id():
    return str(uuid4())  


@app.post("/auth/register")
def register(user: UserRegister):
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Пароль должен содержать минимум 6 символов")
    
    if user.email in users:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже зарегистрирован")
    
    if user.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Роль должна быть 'admin' или 'user'")
    
    user_id = generate_id()
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
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user["user_id"]  
    }


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


@app.get("/routes/environmental", response_model=List[Route])
async def get_eco_routes():
    return eco_routes

@app.post("/routes/environmental", response_model=Route)
async def create_eco_route(route: Route):
    route_id = generate_id()  
    route.id = route_id  
    eco_routes.append(route)  
    return route  

@app.get("/routes/environmental/{route_id}", response_model=Route)
async def get_eco_route(route_id: str):
    route = next((route for route in eco_routes if route.id == route_id), None)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@app.put("/routes/environmental/{route_id}", response_model=Route)
async def update_eco_route(route_id: str, route: Route):
    existing_route = next((r for r in eco_routes if r.id == route_id), None)
    if existing_route:
        existing_route.name = route.name
        existing_route.description = route.description
        existing_route.difficulty = route.difficulty
        existing_route.length_km = route.length_km
        existing_route.eco_friendly = route.eco_friendly
        return existing_route
    raise HTTPException(status_code=404, detail="Route not found")


@app.delete("/routes/environmental/{route_id}", response_model=Route)
async def delete_eco_route(route_id: str):
    route = next((route for route in eco_routes if route.id == route_id), None)
    if route:
        eco_routes.remove(route)
        return route
    raise HTTPException(status_code=404, detail="Route not found")



@app.get("/eco-places", response_model=List[EcoPlace])
async def get_eco_places():
    return eco_places

@app.post("/eco-places", response_model=EcoPlace)
async def create_eco_place(place: EcoPlace):
    place_id = generate_id()  
    print(f"Generated ID: {place_id}")  
    new_place = EcoPlace(
        id=place_id,  
        name=place.name,
        location=place.location,
        description=place.description
    )
    
    eco_places.append(new_place.dict())  
    
    return new_place


@app.get("/eco-places/{place_id}", response_model=EcoPlace)
async def get_eco_place(place_id: str):
    place = next((place for place in eco_places if place["id"] == place_id), None)
    if place:
        return place
    raise HTTPException(status_code=404, detail="Eco-place not found")

@app.put("/eco-places/{place_id}", response_model=EcoPlace)
async def update_eco_place(place_id: str, place: EcoPlace):
    existing_place = next((p for p in eco_places if p["id"] == place_id), None)
    
    if existing_place:
        existing_place["name"] = place.name
        existing_place["location"] = place.location
        existing_place["description"] = place.description
        
        return existing_place
    
    raise HTTPException(status_code=404, detail="Eco-place not found")


@app.delete("/eco-places/{place_id}", response_model=EcoPlace)
async def delete_eco_place(place_id: str):
    place = next((place for place in eco_places if place["id"] == place_id), None)
    if place:
        eco_places.remove(place)
        return place
    raise HTTPException(status_code=404, detail="Eco-place not found")


@app.get("/eco-rewards", response_model=List[Reward])
async def get_eco_rewards():
    return eco_rewards

@app.post("/eco-rewards", response_model=Reward)
async def create_eco_reward(reward: Reward):
    reward_id = generate_id()  
    new_reward = reward.dict()  
    new_reward["id"] = reward_id  
    eco_rewards.append(new_reward) 
    return new_reward  

@app.get("/eco-rewards/{reward_id}", response_model=Reward)
async def get_eco_reward(reward_id: str):
    reward = next((r for r in eco_rewards if r["id"] == reward_id), None)
    if reward:
        return reward
    raise HTTPException(status_code=404, detail="Reward not found")

@app.put("/eco-rewards/{reward_id}", response_model=Reward)
async def update_eco_reward(reward_id: str, reward: Reward):
    existing_reward = next((r for r in eco_rewards if r["id"] == reward_id), None)
    
    if existing_reward:
        existing_reward["name"] = reward.name
        existing_reward["points_needed"] = reward.points_needed
        existing_reward["description"] = reward.description
        return existing_reward  
    
    raise HTTPException(status_code=404, detail="Reward not found")

@app.delete("/eco-rewards/{reward_id}", response_model=Reward)
async def delete_eco_reward(reward_id: str):
    reward = next((r for r in eco_rewards if r["id"] == reward_id), None)
    if reward:
        eco_rewards.remove(reward)
        return reward
    raise HTTPException(status_code=404, detail="Reward not found")
    

@app.get("/eco-actions", response_model=List[EcoAction])
async def get_eco_actions():
    return eco_actions["recycling"] + eco_actions["reusable_stores"]

@app.post("/eco-actions", response_model=EcoAction)
async def create_eco_action(action: EcoAction):
    action_id = generate_id()  
    new_action = action.dict()  
    new_action["id"] = action_id  
    eco_actions[action.action_type].append(new_action)  
    return new_action  


@app.get("/eco-actions/{action_id}", response_model=EcoAction)
async def get_eco_action(action_id: str):
    action = next(
        (action for actions in eco_actions.values() for action in actions if action["id"] == action_id), 
        None
    )
    if action:
        return action
    raise HTTPException(status_code=404, detail="Eco action not found")

@app.put("/eco-actions/{action_id}", response_model=EcoAction)
async def update_eco_action(action_id: str, action: EcoAction):
    for action_list in eco_actions.values():
        existing_action = next((a for a in action_list if a["id"] == action_id), None)
        
        if existing_action:
            existing_action.update({
                key: value for key, value in action.dict().items() if key != "id"
            })
            return existing_action  
    raise HTTPException(status_code=404, detail="Eco action not found")


@app.delete("/eco-actions/{action_id}", response_model=EcoAction)
async def delete_eco_action(action_id: str):
    for action_list in eco_actions.values():
        action = next((action for action in action_list if action["id"] == action_id), None)
        if action:
            action_list.remove(action)
            return action
    raise HTTPException(status_code=404, detail="Eco action not found")


@app.get("/forum", response_model=List[ForumPost])
async def get_forum_posts():
    return community_posts

@app.post("/forum", response_model=ForumPost)
async def create_forum_post(post: ForumPost, token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    user = verify_token(token)
    post.user_email = user["email"]
    post.timestamp = datetime.utcnow()
    post.id = generate_id()
    new_post = post.dict()
    community_posts.append(new_post)
    return post

@app.post("/forum", response_model=ForumPost)
async def create_forum_post(post: ForumPost, token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    post.user_email = user["email"]
    post.timestamp = datetime.utcnow()
    post_id = generate_id()  
    post.id = post_id  

    new_post = post.dict()  
    community_posts.append(new_post)  

    return post  


@app.put("/community/forum/{post_id}", response_model=ForumPost)
async def update_forum_post(post_id: str, post: ForumPost):
    existing_post = next((p for p in community_posts if p["id"] == post_id), None)
    
    if existing_post:
        existing_post["title"] = post.title
        existing_post["content"] = post.content
        existing_post["user_email"] = post.user_email
        existing_post["timestamp"] = post.timestamp
        return existing_post 
    raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/community/forum/{post_id}", response_model=ForumPost)
async def delete_forum_post(post_id: str):
    post = next((p for p in community_posts if p["id"] == post_id), None)
    if post:
        community_posts.remove(post)
        return post
    raise HTTPException(status_code=404, detail="Post not found")
