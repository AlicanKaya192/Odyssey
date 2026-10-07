from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

# require_key: 401 "Invalid API key" unless the X-Api-Key header is "letmein"
# GET /health -> {"status": "ok"} (no key)
# GET /admin/stats -> {"users": 42}, GET /admin/logs -> ["started", "ready"]
#   both require require_key with dependencies=[...]
