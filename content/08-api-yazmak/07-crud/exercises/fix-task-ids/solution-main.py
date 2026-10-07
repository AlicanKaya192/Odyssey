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


@app.get("/tasks")
def list_tasks() -> list[TaskOut]:
    return list(tasks.values())


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
