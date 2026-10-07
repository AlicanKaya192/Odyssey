from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader

app = FastAPI()
KEYS = {"k-ada-1": "ada", "k-alan-2": "alan"}

# APIKeyHeader ile X-API-Key basligini oku (auto_error=False)
# require_api_key: anahtar KEYS'te yoksa 401 "Invalid API key"; varsa sahibinin adini dondur
# GET /reports -> {"owner": ad, "reports": 3}
