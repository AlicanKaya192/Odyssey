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


@asynccontextmanager
async def lifespan(app):
    ml["model"] = train_model()
    yield
    ml.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/model")
def model_info():
    model = ml["model"]
    return {"type": type(model).__name__, "features": int(model.n_features_in_), "classes": SPECIES}


@app.get("/stats")
def show_stats():
    return stats
