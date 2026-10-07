from fastapi import FastAPI, HTTPException

app = FastAPI()
users = {1: {"name": "Ada"}, 2: {"name": "Alan"}}

# GET /users/{user_id} -> kullanici; yoksa 404 "User not found"
# DELETE /users/{user_id} -> 204; yoksa 404 "User not found"
