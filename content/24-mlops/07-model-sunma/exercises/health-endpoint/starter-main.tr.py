from fastapi import FastAPI
from scorer import VERSION

app = FastAPI()

# GET /health: durumu ve model surumunu dondur.
