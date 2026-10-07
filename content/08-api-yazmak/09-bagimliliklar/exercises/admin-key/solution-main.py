from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


def require_key(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key != "letmein":
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/admin/stats", dependencies=[Depends(require_key)])
def stats():
    return {"users": 42}


@app.get("/admin/logs", dependencies=[Depends(require_key)])
def logs():
    return ["started", "ready"]
