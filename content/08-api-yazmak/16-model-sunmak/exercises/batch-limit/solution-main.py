from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
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


@app.post("/predict/batch")
def predict_batch(flowers: list[Flower]):
    if not flowers:
        raise HTTPException(status_code=422, detail="Send at least one flower")
    if len(flowers) > 5:
        raise HTTPException(status_code=413, detail="At most 5 flowers per request")
    labels = ml["model"].predict([to_row(f) for f in flowers])
    return [SPECIES[int(i)] for i in labels]
