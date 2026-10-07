from fastapi import FastAPI

app = FastAPI()


@app.get("/colors")
def colors():
    return ["red", "green", "blue"]
