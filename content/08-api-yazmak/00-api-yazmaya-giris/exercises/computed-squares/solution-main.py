from fastapi import FastAPI

app = FastAPI()


@app.get("/squares")
def squares():
    return [n * n for n in range(1, 11)]
