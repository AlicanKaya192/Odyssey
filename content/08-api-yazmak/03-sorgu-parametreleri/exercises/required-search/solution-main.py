from fastapi import FastAPI

app = FastAPI()


@app.get("/search")
def search(q: str):
    return {"q": q, "length": len(q)}
