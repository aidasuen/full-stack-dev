from fastapi import FastAPI
from typing import List

# Список задач
tasks = []

app = FastAPI()

# Получить все задачи
@app.get("/tasks")
async def get_tasks():
    return tasks

# Получить задачу по ID
@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return {"error": "Task not found"}
    return task

# Добавить новую задачу
@app.post("/tasks")
async def create_task(title: str, description: str = "", done: bool = False):
    task_id = len(tasks) + 1  # Генерация уникального ID
    task = {"id": task_id, "title": title, "description": description, "done": done}
    tasks.append(task)
    return task

# Обновить задачу
@app.put("/tasks/{task_id}")
async def update_task(task_id: int, title: str = None, description: str = None, done: bool = None):
    existing_task = next((t for t in tasks if t['id'] == task_id), None)
    if existing_task is None:
        return {"error": "Task not found"}
    
    # Обновляем данные задачи только если они были переданы
    if title is not None:
        existing_task['title'] = title
    if description is not None:
        existing_task['description'] = description
    if done is not None:
        existing_task['done'] = done
    return existing_task

# Удалить задачу
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return {"message": "Task deleted successfully"}
