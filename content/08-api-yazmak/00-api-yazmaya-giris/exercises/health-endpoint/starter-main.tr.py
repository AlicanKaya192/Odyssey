from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello, API"}


# GET /health istegi {"status": "ok"} dondursun.
