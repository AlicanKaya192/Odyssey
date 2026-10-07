from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# User model: name (string), age (integer)
# POST /users -> {"name", "age", "adult": 18 or over?}
