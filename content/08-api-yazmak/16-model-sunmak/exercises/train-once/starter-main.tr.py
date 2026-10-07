from contextlib import asynccontextmanager

from fastapi import FastAPI
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

SPECIES = ["setosa", "versicolor", "virginica"]
ml = {}
stats = {"trainings": 0}


def train_model():
    stats["trainings"] += 1
    iris = load_iris()
    return LogisticRegression(max_iter=1000).fit(iris.data, iris.target)

app = FastAPI()


# lifespan: acilista ml["model"] = train_model() (BIR KEZ), kapanista ml.clear()
# GET /model -> {"type": modelin sinif adi, "features": n_features_in_ (int), "classes": SPECIES}
# GET /stats -> stats
