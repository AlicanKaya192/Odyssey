from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()
users = {"ada": "admin", "alan": "member"}


def get_user(x_user: Annotated[str | None, Header()] = None) -> dict:
    if x_user not in users:
        raise HTTPException(status_code=401, detail="Unknown user")
    return {"name": x_user, "role": users[x_user]}


def require_admin(user: Annotated[dict, Depends(get_user)]) -> dict:
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user


@app.get("/me")
def me(user: Annotated[dict, Depends(get_user)]):
    return user


@app.get("/admin")
def admin(user: Annotated[dict, Depends(require_admin)]):
    return {"welcome": user["name"]}
