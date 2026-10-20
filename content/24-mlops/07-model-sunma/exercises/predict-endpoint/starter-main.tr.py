from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field
from scorer import VERSION, churn_probability

app = FastAPI()

# Customer modeli: kurallar yonergede.
# POST /predict: olasiligi uc basamaga yuvarla, model surumunu ekle.
