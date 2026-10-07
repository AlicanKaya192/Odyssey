from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()
books = {1: "Dune", 2: "Emma", 3: "Ubik"}


def require_key(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key != "a-secret-you-do-not-know":
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/admin/stats", dependencies=[Depends(require_key)])
def stats():
    return {"books": len(books)}
