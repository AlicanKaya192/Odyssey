from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()
users = {"ada": "admin", "alan": "member"}

# get_user: 401 "Unknown user" if the X-User header isn't in users; otherwise {"name", "role"}
# require_admin: depends on get_user; 403 "Admins only" if the role isn't "admin"; returns the user
# GET /me -> the user (any user)
# GET /admin -> {"welcome": name} (admins only)
