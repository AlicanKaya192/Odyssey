from fastapi import FastAPI

app = FastAPI()
state = {"count": 0}


@app.get("/counter")
def read_counter():
    return state


@app.post("/counter")
def increase():
    state["count"] += 1
    return state


# DELETE /counter: set the counter to 0 and return state
