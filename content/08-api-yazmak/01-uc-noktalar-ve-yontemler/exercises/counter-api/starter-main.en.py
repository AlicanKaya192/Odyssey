from fastapi import FastAPI

app = FastAPI()
state = {"count": 0}

# GET /counter: return state
# POST /counter: increase the number by 1 and return state
