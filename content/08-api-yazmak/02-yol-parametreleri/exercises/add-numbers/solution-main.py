from fastapi import FastAPI

app = FastAPI()


@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"result": a + b}
