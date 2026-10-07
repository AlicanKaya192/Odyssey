from fastapi import FastAPI

app = FastAPI()

# GET /add/{a}/{b} -> {"result": a + b} (a and b are integers)
