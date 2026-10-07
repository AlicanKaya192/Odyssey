from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

# require_key: X-Api-Key basligi "letmein" degilse 401 "Invalid API key"
# GET /health -> {"status": "ok"} (anahtarsiz)
# GET /admin/stats -> {"users": 42}, GET /admin/logs -> ["started", "ready"]
#   ikisi de dependencies=[...] ile require_key istesin
