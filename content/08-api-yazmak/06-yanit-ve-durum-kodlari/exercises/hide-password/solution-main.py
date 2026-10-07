from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
users = {}


class UserIn(BaseModel):
    name: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str


@app.post("/users", status_code=201, response_model=UserOut)
def create_user(user: UserIn):
    new_id = len(users) + 1
    users[new_id] = {"id": new_id, **user.model_dump()}
    return users[new_id]


@app.get("/users", response_model=list[UserOut])
def list_users():
    return list(users.values())
