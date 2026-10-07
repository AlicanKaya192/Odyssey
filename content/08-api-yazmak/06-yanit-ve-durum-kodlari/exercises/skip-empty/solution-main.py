from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
profiles = {
    1: {"name": "Ada", "bio": "Mathematician", "website": None, "secret_note": "x"},
    2: {"name": "Alan", "bio": None, "website": "https://example.com", "secret_note": "y"},
}


class Profile(BaseModel):
    name: str
    bio: str | None = None
    website: str | None = None


@app.get("/profiles/{profile_id}", response_model=Profile, response_model_exclude_none=True)
def get_profile(profile_id: int):
    return profiles[profile_id]
