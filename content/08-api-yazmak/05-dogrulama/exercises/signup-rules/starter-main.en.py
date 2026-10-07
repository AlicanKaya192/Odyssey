from fastapi import FastAPI
from pydantic import BaseModel, field_validator

app = FastAPI()

# Signup model: username, email
#   username: letters and digits only (no spaces, dots); lower-case it
#   email: must contain @
# Raise ValueError when a rule breaks. POST /signup -> return the model
