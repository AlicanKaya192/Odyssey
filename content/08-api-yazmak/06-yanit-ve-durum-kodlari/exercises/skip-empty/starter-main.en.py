from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
profiles = {
    1: {"name": "Ada", "bio": "Mathematician", "website": None, "secret_note": "x"},
    2: {"name": "Alan", "bio": None, "website": "https://example.com", "secret_note": "y"},
}

# Profile model: name (required), bio and website (str | None, default None)
# GET /profiles/{profile_id} -> Profile; fields that are None must NOT be in the answer,
#   and secret_note must not go out
