from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

SPECIES = ["setosa", "versicolor", "virginica"]
ml = {}
stats = {"trainings": 0}


def train_model():
    stats["trainings"] += 1
    iris = load_iris()
    return LogisticRegression(max_iter=1000).fit(iris.data, iris.target)


@asynccontextmanager
async def lifespan(app):
    ml["model"] = train_model()
    yield
    ml.clear()


app = FastAPI(lifespan=lifespan)


class Flower(BaseModel):
    sepal_length: float = Field(gt=0, le=10)
    sepal_width: float = Field(gt=0, le=10)
    petal_length: float = Field(gt=0, le=10)
    petal_width: float = Field(gt=0, le=10)


def to_row(flower: Flower) -> list:
    return [flower.sepal_length, flower.sepal_width, flower.petal_length, flower.petal_width]


@app.post("/predict")
def predict(flower: Flower):
    row = [to_row(flower)]
    label = int(ml["model"].predict(row)[0])
    proba = ml["model"].predict_proba(row)[0]
    return {"label": label, "species": SPECIES[label],
            "probabilities": [round(p, 3) for p in proba.tolist()]}
