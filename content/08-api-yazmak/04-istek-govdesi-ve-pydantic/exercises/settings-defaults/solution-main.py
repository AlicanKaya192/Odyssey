from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Settings(BaseModel):
    theme: str = "dark"
    font_size: int = 14
    beta: bool = False


@app.post("/settings")
def save_settings(settings: Settings):
    return settings
