from fastapi import FastAPI
from pydantic import BaseModel, field_validator

app = FastAPI()


class Signup(BaseModel):
    username: str
    email: str

    @field_validator("username")
    @classmethod
    def clean_username(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("only letters and digits")
        return value.lower()

    @field_validator("email")
    @classmethod
    def has_at(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("not an email address")
        return value


@app.post("/signup")
def signup(data: Signup):
    return data
