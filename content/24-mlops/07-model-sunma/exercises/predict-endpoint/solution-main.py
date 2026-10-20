from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field
from scorer import VERSION, churn_probability

app = FastAPI()


class Customer(BaseModel):
    tenure: int = Field(ge=1, le=72)
    monthly_fee: float = Field(ge=5, le=100)
    support_calls: int = Field(ge=0, le=10)
    usage_hours: float = Field(ge=0, le=100)
    plan: Literal["basic", "pro"]


@app.post("/predict")
def predict(customer: Customer):
    probability = churn_probability(customer.model_dump())
    return {"churn_probability": round(probability, 3), "model_version": VERSION}
