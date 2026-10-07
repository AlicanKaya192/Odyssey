from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
users = {}

# UserIn: name, password (incoming body)
# UserOut: id, name (outgoing answer; NO password)
# POST /users -> 201, store the record in users (with password), return it as UserOut
# GET /users -> all users, as a list of UserOut
