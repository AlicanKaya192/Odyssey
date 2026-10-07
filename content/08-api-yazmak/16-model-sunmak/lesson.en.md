# Serving an ML Model

In the Machine Learning track you trained models and got predictions with
`predict`; but those models only ran in your notebook. What if an app or a
website wants to use one? The answer is this whole track: putting the model
**behind an API**. The client sends the measurements, the API returns the
prediction.

In this section you serve a model using the **iris** data that comes with
scikit-learn (flowers' sepal and petal measurements → three species).

## Two separate jobs: training and serving

| | Training | Serving |
|---|---|---|
| When? | Once, now and then | Constantly, on every request |
| What does it do? | Makes a model from data | Predicts with a ready model |
| Time | Seconds, hours | Milliseconds |

Training is done in a separate script and the model is saved to a **file**:

```python
# train.py
import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

iris = load_iris()
model = LogisticRegression(max_iter=1000).fit(iris.data, iris.target)
joblib.dump(model, "model.joblib")
```

`joblib.dump` writes the model to disk as it is (this model is 991 bytes);
`joblib.load` reads it back (we measured: 0.001 s). The API doesn't train, it
only loads.

## Loading the model once

The `lifespan` from the async section is made for exactly this:

```python
from contextlib import asynccontextmanager

import joblib
from fastapi import FastAPI

ml = {}


@asynccontextmanager
async def lifespan(app):
    ml["model"] = joblib.load("model.joblib")
    yield
    ml.clear()


app = FastAPI(lifespan=lifespan)
```

The model is loaded once while the server starts, not on every request.
With big models (hundreds of MB) the difference is huge.

## Validating the input

A model doesn't fail on wrong input; it gives a **nonsense** prediction.
That's why checking at the door is the API's job, not the model's:

```python
from pydantic import BaseModel, Field


class Flower(BaseModel):
    sepal_length: float = Field(gt=0, le=10)
    sepal_width: float = Field(gt=0, le=10)
    petal_length: float = Field(gt=0, le=10)
    petal_width: float = Field(gt=0, le=10)
```

A missing measurement or a negative length never reaches the model (`422`).

## The prediction endpoint

```python
SPECIES = ["setosa", "versicolor", "virginica"]


@app.post("/predict")
def predict(flower: Flower):
    row = [[flower.sepal_length, flower.sepal_width,
            flower.petal_length, flower.petal_width]]
    label = int(ml["model"].predict(row)[0])
    proba = ml["model"].predict_proba(row)[0]
    return {"species": SPECIES[label],
            "probability": round(float(proba[label]), 3)}
```

- `row` is two-dimensional: a **one-row** table. scikit-learn wants even a
  single example as a table (remember from the ML track:
  `Expected 2D array`).
- The column order must be the **same** as in training; the model knows the
  order, not the column names.
- `int(...)` and `float(...)`: see below for why.

We measured:

```text
POST /predict  5.1, 3.5, 1.4, 0.2   200 {"species": "setosa", "probability": 0.982}
POST /predict  6.7, 3.0, 5.2, 2.3   200 {"species": "virginica", "probability": 0.92}
POST /predict  5.9, 3.0, 4.2, 1.5   200 {"species": "versicolor", "probability": 0.899}
POST /predict  sepal_length: -1     422 greater_than
POST /predict  no petal_width       422 missing
```

<figure class="fig">
  <div class="flow">
    <span class="node">POST /predict<br><small>4 measurements</small></span><span class="arrow">→</span>
    <span class="node acc">Flower<br><small>validation</small></span><span class="arrow">→</span>
    <span class="node">model.predict([[...]])<br><small>loaded in lifespan</small></span><span class="arrow">→</span>
    <span class="node ok">{"species": "setosa"}<br><small>int(), float()</small></span>
  </div>
  <figcaption>Validation at the door, a model loaded once in the middle, NumPy values turned into Python at the exit.</figcaption>
</figure>

## The NumPy trap

`predict` returns a NumPy array; the value inside isn't Python's `int` but
NumPy's `int64`. We put it straight into the answer:

```python
return {"label": ml["model"].predict(row)[0]}
```

```text
POST /predict   500 Internal Server Error
```

FastAPI couldn't turn the NumPy number into JSON (we measured). The fix:
`int(...)`, `float(...)`, and `.tolist()` for lists, before putting them in
the answer. Convert **every** value that comes from the model this way.

## Several predictions

```python
@app.post("/predict/batch")
def predict_batch(flowers: list[Flower]):
    rows = [[f.sepal_length, f.sepal_width, f.petal_length, f.petal_width]
            for f in flowers]
    labels = ml["model"].predict(rows)
    return [SPECIES[int(i)] for i in labels]
```

The body is a list; the model predicts them all in one go (much faster than
a separate request for each). We measured: two flowers →
`["setosa", "virginica"]`.

## The model's identity

The client should know which model it's talking to; answers may change when
a new model is loaded:

```python
@app.get("/model")
def model_info():
    model = ml["model"]
    return {"type": type(model).__name__, "classes": SPECIES,
            "features": int(model.n_features_in_)}
```

```text
GET /model  200 {"type": "LogisticRegression", "classes": [...], "features": 4}
```

In real projects the model's version, its training date and its validation
score are written here too.

## The road to Docker

To run this API on another computer, take the road from the Docker track:
`main.py` + `model.joblib` + `requirements.txt` go into an image, started
with `uvicorn main:app --host 0.0.0.0`. The end of API 2 is the beginning of
opening your model to the world.

## Summary

- Training is separate (`joblib.dump`), serving is separate (`joblib.load`,
  once in `lifespan`).
- The input is validated with Pydantic; a model doesn't fail on nonsense
  input.
- `predict` wants two-dimensional input; the column order matches training.
- NumPy values are converted with `int()` / `float()` / `.tolist()`;
  otherwise `500`.
- Batch predictions in one call; `/model` tells which model is running.
