from fastapi import FastAPI

app = FastAPI()
lamp = {"on": False}


@app.get("/lamp")
def read_lamp():
    return lamp


@app.post("/lamp/toggle")
def toggle():
    lamp["on"] = not lamp["on"]
    return lamp
