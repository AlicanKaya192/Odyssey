from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator

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


# TaskPatch: title (str | None, min 1 karakter), done (bool | None); ikisinin de varsayilani None
#   gonderilen null -> 422 (field_validator)
# PATCH /tasks/{task_id} -> yalnizca gonderilen alanlari degistir, guncel gorevi dondur; yoksa 404
