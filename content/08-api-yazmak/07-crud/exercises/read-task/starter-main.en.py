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


# find_task(task_id): 404 "Task not found" if missing, otherwise returns the task
# GET /tasks?done=true|false -> (optional) filter by done
# GET /tasks/{task_id} -> the task or 404
