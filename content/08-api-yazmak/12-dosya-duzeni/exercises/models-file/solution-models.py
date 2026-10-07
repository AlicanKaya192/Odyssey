from pydantic import BaseModel, Field


class BookIn(BaseModel):
    title: str = Field(min_length=1)
    year: int = Field(ge=1450, le=2100)
