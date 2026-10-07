from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
notes = []

# Note model: text (a required string), pinned (bool, default False)
# POST /notes -> 201, {"id": ..., "text": ..., "pinned": ...}
# GET /notes -> the list of added notes
