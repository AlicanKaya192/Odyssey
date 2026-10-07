from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader

app = FastAPI()
KEYS = {"k-ada-1": "ada", "k-alan-2": "alan"}

# Read the X-API-Key header with APIKeyHeader (auto_error=False)
# require_api_key: 401 "Invalid API key" if the key isn't in KEYS; otherwise return its owner's name
# GET /reports -> {"owner": name, "reports": 3}
