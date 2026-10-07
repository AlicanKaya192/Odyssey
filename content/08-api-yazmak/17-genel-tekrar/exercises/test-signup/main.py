from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
emails = set()


class Signup(BaseModel):
    email: str = Field(min_length=3)
    age: int = Field(ge=13)


@app.post("/signup", status_code=201)
def signup(data: Signup):
    email = data.email.lower()
    if email in emails:
        raise HTTPException(status_code=409, detail="Email already registered")
    emails.add(email)
    return {"email": email}
