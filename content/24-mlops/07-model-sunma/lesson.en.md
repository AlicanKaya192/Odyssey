# Packaging and Serving a Model

The model is in the registry, it passed the gate, it got the
`production` alias. But as long as it sits on the disk as a file, it is
of no use to anyone. **Serving** means getting the model's predictions to
the person or program that will use them. In the Writing REST APIs with
FastAPI module you saw how to serve a model as an API; in this section we
look at the MLOps side of it: loading the registered file safely,
deciding between batch and online prediction, putting the model version
in the answer, measuring speed correctly, and packaging it all into an
image.

## The saved model

First let's prepare the model we will serve: train it, write it to a
file, and put its registry information (name, version, hash) next to it:

```python
import hashlib
import json
import pickle
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from ml_data import make_customers, NUMERIC


def features(row):
    return [row[c] for c in NUMERIC] + [1 if row["plan"] == "pro" else 0]


rows = make_customers(2000)
model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=0)
model.fit([features(r) for r in rows], [r["churned"] for r in rows])
data = pickle.dumps(model)
Path("model.pkl").write_bytes(data)
digest = hashlib.sha256(data).hexdigest()
card = {"name": "churn", "version": 3, "sha256": digest}
Path("model.json").write_text(json.dumps(card), encoding="utf-8")
print("model file:", len(data), "bytes")
```

```text
model file: 1966988 bytes
```

A file of about 2 MB. The serving program has to open it and rebuild 100
trees in memory.

## Load it once

The most common mistake is loading the model again **on every request**.
Let's look with a counter that counts how many times it is loaded:

```python
loads = {"count": 0}


def load_model():
    loads["count"] += 1
    return pickle.loads(Path("model.pkl").read_bytes())


requests = make_customers(100, seed=5)
for row in requests:
    load_model().predict_proba([features(row)])
print("loads for 100 requests, reloading:", loads["count"])

loads["count"] = 0
loaded = load_model()
for row in requests:
    loaded.predict_proba([features(row)])
print("loads for 100 requests, loaded once:", loads["count"])
```

```text
loads for 100 requests, reloading: 100
loads for 100 requests, loaded once: 1
```

In the first way, every request reads the disk and rebuilds the 100
trees from scratch; in the second this work is done once, when the
program starts. The bigger the model, the bigger the difference: if a
model of a hundred megabytes is loaded on every request, a request takes
seconds. The rule: the model is loaded once **when the program starts**,
and requests use the same object in memory.

## Batch or online?

Predictions are wanted in two ways:

- **Batch prediction:** at regular times (every night, say) all customers
  are scored at once and the results are written to a table. In the
  morning the customer team looks at the list and decides whom to call.
- **Online prediction:** a request comes in and the answer goes back at
  once. Like showing an offer to a customer the moment they open the
  cancellation page.

If the need allows waiting, batch prediction is both simpler and
cheaper. A model is much faster when it handles rows together rather
than one by one:

```python
import time

batch = [features(r) for r in make_customers(1000, seed=6)]
start = time.perf_counter()
loaded.predict_proba(batch)
per_row_batch = (time.perf_counter() - start) / len(batch)
start = time.perf_counter()
for x in batch[:50]:
    loaded.predict_proba([x])
per_row_single = (time.perf_counter() - start) / 50
faster = per_row_batch * 10 < per_row_single
print("batch is at least 10x faster per customer:", faster)
```

```text
batch is at least 10x faster per customer: True
```

Times differ on every computer; that is why we printed the comparison,
not the time. A prediction call has a fixed setup cost; in a batch call
that cost is shared by 1000 customers.

## The batch scoring job

Batch prediction is often a small script: read the file, score it, write
the result. The values read from the CSV are text, so `from_csv` turns
them into numbers. It matters to write the **model version** into the
result file too: three months later, when someone asks "why did we call
this customer?", it must be known which model decided.

```python
import csv
from ml_data import write_customers_csv

write_customers_csv("customers.csv", 1000, seed=6)
with open("customers.csv", encoding="utf-8") as f:
    customers = list(csv.DictReader(f))


def from_csv(r):
    return [float(r[c]) for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


X = [from_csv(r) for r in customers]
probabilities = loaded.predict_proba(X)[:, 1]
with open("scores.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(["id", "churn_probability", "model_version"])
    for row, p in zip(customers, probabilities):
        writer.writerow([row["id"], round(float(p), 3), card["version"]])
for line in Path("scores.csv").read_text(encoding="utf-8").splitlines()[:4]:
    print(line)
print("customers to call:", int((probabilities >= 0.5).sum()))
```

```text
id,churn_probability,model_version
C00-00001,0.035,3
C00-00002,0.091,3
C00-00003,0.009,3
customers to call: 226
```

## Online prediction: an API

For online prediction let's build an API. It is the same structure as in
the Writing REST APIs with FastAPI module; from the MLOps point of view, three things are
added:

1. The model is loaded **at startup** (`lifespan`) and the file's hash is
   compared with the registry's: if it doesn't match, the program never
   starts.
2. The input is checked with the rules from the Data Validation section;
   a request that breaks the rules gets a clear `422`, not a silently
   wrong prediction.
3. Every answer and the health endpoint carry the **model version**.

```python
from contextlib import asynccontextmanager
from typing import Literal
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

state = {}


@asynccontextmanager
async def lifespan(app):
    info = json.loads(Path("model.json").read_text(encoding="utf-8"))
    data = Path("model.pkl").read_bytes()
    if hashlib.sha256(data).hexdigest() != info["sha256"]:
        raise RuntimeError("model.pkl does not match model.json")
    state["model"], state["version"] = pickle.loads(data), info["version"]
    yield
    state.clear()


app = FastAPI(lifespan=lifespan)


class Customer(BaseModel):
    tenure: int = Field(ge=1, le=72)
    monthly_fee: float = Field(ge=5, le=100)
    support_calls: int = Field(ge=0, le=10)
    usage_hours: float = Field(ge=0, le=100)
    plan: Literal["basic", "pro"]


@app.get("/health")
def health():
    return {"status": "ok", "model_version": state["version"]}


@app.post("/predict")
def predict(customer: Customer):
    row = customer.model_dump()
    probability = float(state["model"].predict_proba([features(row)])[0, 1])
    return {"churn_probability": round(probability, 3),
            "model_version": state["version"]}


good = {"tenure": 2, "monthly_fee": 45.0, "support_calls": 6,
        "usage_hours": 5.0, "plan": "pro"}
with TestClient(app) as client:
    print(client.get("/health").json())
    print(client.post("/predict", json=good).json())
    print(client.post("/predict", json={**good, "plan": "PRO"}).status_code)
```

```text
{'status': 'ok', 'model_version': 3}
{'churn_probability': 0.901, 'model_version': 3}
422
```

`Literal["basic", "pro"]` says the field can take only one of these two
values; that is why `"PRO"` got `422`. `model_dump()` turns the Pydantic
object into a dictionary, so **the same** `features` function as in
training is used. Training and serving using the same code is very
important; that is exactly the topic of the next section.

The `with TestClient(app) as client:` block runs the `lifespan` too: the
model is loaded as the block starts.

## Measuring speed correctly

An API's speed is measured by its **latency**: how long it takes for a
request's answer to arrive. The average latency is misleading. Let's look
at the times of twenty requests; two of them are slow:

```python
import math


def percentile(values, p):
    ordered = sorted(values)
    rank = math.ceil(p / 100 * len(ordered))
    return ordered[rank - 1]


latencies_ms = [12, 15, 11, 14, 13, 90, 12, 16, 13, 14,
                12, 15, 13, 11, 14, 12, 13, 15, 14, 250]
print("average:", sum(latencies_ms) / len(latencies_ms))
print("p50:", percentile(latencies_ms, 50))
print("p95:", percentile(latencies_ms, 95))
```

```text
average: 28.95
p50: 13
p95: 90
```

The average is 28.95 ms: a number no request actually experienced.
**Percentiles** are used instead:

- **p50** (the median): half of the requests are faster than this. What
  the typical user sees.
- **p95**: 95 percent of the requests are faster than this. What the user
  having a slow day sees.

Speed promises are usually made in terms of p95 or p99: "95 percent of
requests under 100 ms". `math.ceil` rounds a number up; `rank` is which
element of the sorted list to look at.

## Packaging into an image

In the Docker path you saw how to put a Python application into an image.
For an application that serves a model there are a few extra rules:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py model.pkl model.json ./
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

- The versions in `requirements.txt` are **the same as in training** and
  pinned with `==`. A model saved with one version can warn or behave
  differently when opened with another (the Machine Learning Libraries
  module).
- The model file is inside the image. The image's tag carries the model
  version (like `churn-api:3`): which image serves which model is clear.
  The other way is for the image to download the model from the registry
  by the `production` alias at startup; then the model can change without
  the image changing, but startup depends on the network and the
  registry.
- The program loads the model at startup, so it is ready before the first
  request arrives. The health endpoint (`/health`) also says the model
  version; after a deployment, a single request confirms that the right
  model is in production.

## Summary

- **Serving** is getting a model's predictions to where they will be
  used.
- The model is loaded **once** when the program starts; loading it on
  every request is wasted work and slowness.
- **Batch prediction** is simpler and cheaper for work that can wait;
  **online prediction** is for places where the answer is needed at once.
- The **model version** is always written next to a prediction.
- The API checks the input with the training rules and uses **the same**
  feature code as training.
- Speed is measured with **percentiles** (p50, p95); the average hides
  slow requests.
- In the image, the library versions are the same as in training; the
  image's tag carries the model version.
