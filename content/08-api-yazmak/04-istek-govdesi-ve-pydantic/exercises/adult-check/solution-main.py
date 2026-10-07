from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str
    age: int


@app.post("/users")
def check_user(user: User):
    return {"name": user.name, "age": user.age, "adult": user.age >= 18}
