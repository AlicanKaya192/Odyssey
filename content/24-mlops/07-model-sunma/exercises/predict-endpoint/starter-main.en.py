from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field
from scorer import VERSION, churn_probability

app = FastAPI()

# The Customer model: the rules are in the instructions.
# POST /predict: round the probability to three digits, add the model version.
