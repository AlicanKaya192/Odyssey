from fastapi import FastAPI, HTTPException

app = FastAPI()
shelves = {
    1: ["Dune", "Emma"],
    2: [],
    3: ["Ulysses"],
}

# GET /users/{user_id}/books
#   -> {"user_id": ..., "books": [...], "count": ...}
#   kullanici yoksa 404 "User not found"
