from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
profiles = {
    1: {"name": "Ada", "bio": "Mathematician", "website": None, "secret_note": "x"},
    2: {"name": "Alan", "bio": None, "website": "https://example.com", "secret_note": "y"},
}

# Profile modeli: name (zorunlu), bio ve website (str | None, varsayilan None)
# GET /profiles/{profile_id} -> Profile; None olan alanlar cevapta OLMASIN,
#   secret_note da gitmesin
