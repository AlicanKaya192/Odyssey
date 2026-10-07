from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
notes = []

# Note modeli: text (zorunlu metin), pinned (bool, varsayilan False)
# POST /notes -> 201, {"id": ..., "text": ..., "pinned": ...}
# GET /notes -> eklenen notlarin listesi
