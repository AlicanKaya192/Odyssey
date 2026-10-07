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


class TaskPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    done: bool | None = None

    @field_validator("title", "done")
    @classmethod
    def not_null(cls, value):
        if value is None:
            raise ValueError("may not be null")
        return value


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, patch: TaskPatch) -> TaskOut:
    record = find_task(task_id)
    record.update(patch.model_dump(exclude_unset=True))
    return record
