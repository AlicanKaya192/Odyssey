from fastapi import FastAPI

app = FastAPI()

# GET /search?q=... -> {"q": q, "length": the length of q}
# q is required: 422 if not sent
