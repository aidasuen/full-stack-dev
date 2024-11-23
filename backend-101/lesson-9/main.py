from fastapi import FastAPI

# Создаем экземпляр приложения
app = FastAPI()

# Обработчик GET-запроса на корневой путь "/"
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

