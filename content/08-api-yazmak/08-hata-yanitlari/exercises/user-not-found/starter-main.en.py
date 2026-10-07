from fastapi import FastAPI, HTTPException

app = FastAPI()
users = {1: {"name": "Ada"}, 2: {"name": "Alan"}}

# GET /users/{user_id} -> the user; 404 "User not found" if missing
# DELETE /users/{user_id} -> 204; 404 "User not found" if missing
