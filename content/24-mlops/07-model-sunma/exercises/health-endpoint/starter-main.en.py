from fastapi import FastAPI
from scorer import VERSION

app = FastAPI()

# GET /health: return the status and the model version.
