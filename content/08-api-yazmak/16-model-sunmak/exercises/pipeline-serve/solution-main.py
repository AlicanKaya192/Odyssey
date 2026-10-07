from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SPECIES = ["setosa", "versicolor", "virginica"]
ml = {}


def train_model():
    iris = load_iris()
    return make_pipeline(StandardScaler(), KNeighborsClassifier()).fit(iris.data, iris.target)


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
    label = int(ml["model"].predict([to_row(flower)])[0])
    return {"species": SPECIES[label]}
