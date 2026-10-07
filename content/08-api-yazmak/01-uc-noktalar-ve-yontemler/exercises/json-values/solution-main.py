from fastapi import FastAPI

app = FastAPI()


@app.get("/pi")
def pi():
    return 3.14159


@app.get("/name")
def name():
    return "Odyssey"


@app.get("/empty")
def empty():
    return None
