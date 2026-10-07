from fastapi import FastAPI

app = FastAPI()


@app.get("/helo")
def hello():
    return {"greeting": "hi"}
