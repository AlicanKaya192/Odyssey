from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
names = {"ada"}


class Signup(BaseModel):
    name: str


@app.post("/signup", status_code=201)
def signup(data: Signup):
    name = data.name.lower()
    if name in names:
        raise HTTPException(status_code=409,
                            detail={"code": "name_taken", "name": name})
    names.add(name)
    return {"name": name}
