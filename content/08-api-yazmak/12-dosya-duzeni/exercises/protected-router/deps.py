from typing import Annotated

from fastapi import Header, HTTPException


def require_key(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key != "letmein":
        raise HTTPException(status_code=401, detail="Invalid API key")
