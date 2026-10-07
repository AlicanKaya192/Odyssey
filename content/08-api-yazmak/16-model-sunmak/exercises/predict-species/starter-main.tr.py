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


# Flower: dort olcu (sepal_length, sepal_width, petal_length, petal_width), her biri 0 < x <= 10
# POST /predict -> {"species": SPECIES[tahmin]}
#   satir: [[sepal_length, sepal_width, petal_length, petal_width]] (bu sirayla!)
