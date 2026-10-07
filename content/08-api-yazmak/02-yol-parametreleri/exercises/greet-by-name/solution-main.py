from fastapi import FastAPI

app = FastAPI()


@app.get("/hello/{name}")
def hello(name: str):
    return {"greeting": "Hello, " + name}
