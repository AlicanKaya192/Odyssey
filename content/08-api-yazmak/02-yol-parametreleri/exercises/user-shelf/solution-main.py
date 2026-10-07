from fastapi import FastAPI, HTTPException

app = FastAPI()
shelves = {
    1: ["Dune", "Emma"],
    2: [],
    3: ["Ulysses"],
}


@app.get("/users/{user_id}/books")
def user_books(user_id: int):
    if user_id not in shelves:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "books": shelves[user_id], "count": len(shelves[user_id])}
