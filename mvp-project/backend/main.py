from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import auth, routes, ecoplaces, rewards, ecoactions, forum, admin

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Accept", "Authorization"],
)

try:
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы в базе данных")
except Exception as e:
    print(f"Ошибка при создании таблиц: {e}")
    raise

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(routes.router, prefix="/routes", tags=["routes"])
app.include_router(ecoplaces.router, prefix="/eco-places", tags=["eco-places"])
app.include_router(rewards.router, prefix="/eco-rewards", tags=["eco-rewards"])
app.include_router(ecoactions.router, prefix="/eco-actions", tags=["eco-actions"])
app.include_router(forum.router, prefix="/forum", tags=["forum"])
app.include_router(admin.router)