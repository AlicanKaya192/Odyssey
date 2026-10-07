from fastapi import FastAPI

app = FastAPI()
lamp = {"on": False}

# GET /lamp: the lamp's state
# POST /lamp/toggle: switch it off if on, on if off; return the new state
