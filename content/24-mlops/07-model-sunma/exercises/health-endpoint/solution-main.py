from fastapi import FastAPI
from scorer import VERSION

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok", "model_version": VERSION}
