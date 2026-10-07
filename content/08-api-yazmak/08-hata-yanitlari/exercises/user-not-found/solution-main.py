from fastapi import FastAPI, HTTPException

app = FastAPI()
users = {1: {"name": "Ada"}, 2: {"name": "Alan"}}


@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
