from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader

app = FastAPI()
KEYS = {"k-ada-1": "ada", "k-alan-2": "alan"}
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(key: Annotated[str | None, Depends(api_key_header)]) -> str:
    if key not in KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return KEYS[key]


@app.get("/reports")
def reports(owner: Annotated[str, Depends(require_api_key)]):
    return {"owner": owner, "reports": 3}
