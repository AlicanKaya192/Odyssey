from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Settings model: theme ("dark"), font_size (14), beta (False) - all have defaults
# POST /settings -> return the model as it is
