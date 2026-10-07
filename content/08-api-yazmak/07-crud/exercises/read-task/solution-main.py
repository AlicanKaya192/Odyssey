from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
tasks = {}
next_id = 1


class TaskIn(BaseModel):
    title: str = Field(min_length=1)
    done: bool = False


class TaskOut(TaskIn):
    id: int


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskIn) -> TaskOut:
    global next_id
    record = {"id": next_id, **task.model_dump()}
    tasks[next_id] = record
    next_id += 1
    return record


def find_task(task_id: int) -> dict:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.get("/tasks")
def list_tasks(done: bool | None = None) -> list[TaskOut]:
    result = list(tasks.values())
    if done is not None:
        result = [t for t in result if t["done"] == done]
    return result


@app.get("/tasks/{task_id}")
def read_task(task_id: int) -> TaskOut:
    return find_task(task_id)
