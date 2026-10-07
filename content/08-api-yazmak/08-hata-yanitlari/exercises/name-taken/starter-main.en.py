from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
names = {"ada"}


class Signup(BaseModel):
    name: str


# POST /signup -> lower-case the name; if it's in names, 409,
#   detail {"code": "name_taken", "name": name}; otherwise add it, 201 {"name": name}
