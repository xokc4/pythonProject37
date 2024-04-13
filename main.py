from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Модель данных для задачи
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    status: bool = False

# Хранилище задач (заглушка)
tasks_db = []
task_id = 0

# Конечная точка для получения списка всех задач
@app.get("/tasks", response_model=List[Task], tags=["tasks"])
async def read_tasks():
    """Получить список всех задач"""
    return tasks_db

# Конечная точка для получения задачи по идентификатору
@app.get("/tasks/{task_id}", response_model=Task, tags=["tasks"])
async def read_task(task_id: int):
    """Получить задачу по идентификатору"""
    task = next((task for task in tasks_db if task.get("id") == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Конечная точка для добавления новой задачи
@app.post("/tasks", response_model=Task, tags=["tasks"])
async def create_task(task: Task):
    """Добавить новую задачу"""
    global task_id
    task_id += 1
    task_data = task.dict()
    task_data["id"] = task_id
    tasks_db.append(task_data)
    return task_data

# Конечная точка для обновления задачи по идентификатору
@app.put("/tasks/{task_id}", response_model=Task, tags=["tasks"])
async def update_task(task_id: int, task: Task):
    """Обновить задачу по идентификатору"""
    index = next((index for index, t in enumerate(tasks_db) if t.get("id") == task_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db[index] = {"id": task_id, **task.dict()}
    return tasks_db[index]

# Конечная точка для удаления задачи по идентификатору
@app.delete("/tasks/{task_id}", tags=["tasks"])
async def delete_task(task_id: int):
    """Удалить задачу по идентификатору"""
    global tasks_db
    tasks_db = [task for task in tasks_db if task.get("id") != task_id]
    return {"message": "Task deleted"}

@app.get("/", response_class=HTMLResponse)
async def root():
    """Открыть документацию Swagger UI"""
    return """
    <html>
        <head>
            <title>Task API</title>
        </head>
        <body>
            <h1>Welcome to Task API</h1>
            <p>You can find the documentation <a href="/docs">here</a>.</p>
        </body>
    </html>
    """
