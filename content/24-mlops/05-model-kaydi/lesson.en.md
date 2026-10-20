# The Model Registry

The folder has `model.pkl`, `model_new.pkl`, `model_final.pkl` and
`model_final_real.pkl`. Which one is giving predictions to customers
right now? Which one was better? If the new one turns out bad, how do you
go back to the old one? The answers to these questions are not in the
file names but in a **model registry**. In this section we build a small
model registry: numbered versions of every model, labels that say which
version is in production, and a gate a new version must pass before it
goes into production.

## The evaluation set

To compare versions we must measure them all on the **same** data. Let's
set aside an evaluation set that never changes and write a function that
trains models and measures them on this set:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X_hold, y_hold = to_xy(make_customers(1000, seed=99))


def train(kind, rows):
    if kind == "logistic":
        model = make_pipeline(StandardScaler(), LogisticRegression())
    else:
        model = RandomForestClassifier(n_estimators=100, random_state=0)
    model.fit(*to_xy(rows))
    return model, round(model.score(X_hold, y_hold), 3)


model_1, accuracy_1 = train("logistic", make_customers(2000))
print("first model:", accuracy_1)
```

```text
first model: 0.813
```

## The registry: version numbers

Let the registry be a JSON file. Under every model name there is a list
of versions; every version carries its number, its file, its file's
hash, its measurements and a short note:

```python
import hashlib
import json
import pickle
from pathlib import Path

REGISTRY = Path("registry.json")
MODELS = Path("models")


def read_registry():
    if not REGISTRY.exists():
        return {}
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def write_registry(registry):
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")


def register(name, model, metrics, note):
    registry = read_registry()
    empty = {"versions": [], "aliases": {}, "history": []}
    entry = registry.setdefault(name, empty)
    version = len(entry["versions"]) + 1
    data = pickle.dumps(model)
    MODELS.mkdir(exist_ok=True)
    path = MODELS / f"{name}-v{version}.pkl"
    path.write_bytes(data)
    entry["versions"].append({"version": version, "file": path.as_posix(),
                              "sha256": hashlib.sha256(data).hexdigest(),
                              "metrics": metrics, "note": note})
    write_registry(registry)
    return version


v1 = register("churn", model_1, {"accuracy": accuracy_1}, "logistic")
print("registered version:", v1)
for key, value in read_registry()["churn"]["versions"][0].items():
    print(f"{key:>8}: {value}")
```

```text
registered version: 1
 version: 1
    file: models/churn-v1.pkl
  sha256: 5d94979f5608ab49cfc694e7530a88737ea8c2acbe5c070ef20e499578ba1b16
 metrics: {'accuracy': 0.813}
    note: logistic
```

A few details:

- `setdefault` opens an empty entry if the model name isn't in the
  registry, and gives the existing one otherwise. That is how the first
  version comes about on its own.
- The version number grows and is **never reused**. When someone says
  "version 3", everyone means the same file.
- The file's hash is in the registry: as in the Data and Model Versioning
  section, if the file changes later, it is noticed.
- `as_posix()` writes the path with `/`, so that the registry looks the
  same on every operating system.

## Aliases: which version is in production?

Version numbers don't change; but "the model in production" does. We
say it with a **label** (alias): whichever version the `production`
alias points at is the model in production. The prediction code doesn't
know version numbers; it only asks for the alias:

```python
def set_alias(name, alias, version):
    registry = read_registry()
    entry = registry[name]
    entry["aliases"][alias] = version
    entry["history"].append([alias, version])
    write_registry(registry)


def load_model(name, alias):
    entry = read_registry()[name]
    version = entry["aliases"][alias]
    info = entry["versions"][version - 1]
    data = Path(info["file"]).read_bytes()
    if hashlib.sha256(data).hexdigest() != info["sha256"]:
        raise ValueError(f"{info['file']} does not match the registry")
    return version, pickle.loads(data)


set_alias("churn", "production", 1)
version, model = load_model("churn", "production")
print("production is version", version)
print("first predictions:", model.predict(X_hold[:5]).tolist())
```

```text
production is version 1
first predictions: [0, 0, 0, 0, 0]
```

The beauty of this: to change the model in production, there's no need
to change the prediction code or release it again. Pointing the alias at
another version is enough. Every alias change is also written into the
`history` list: which version went into production, and in what order.

`load_model` compares the file's hash with the one in the registry
before opening it: a file that is not in the registry cannot reach
production.

## The gate: who goes into production?

A new version should not go into production just because it was
registered. First it must show that it is **better** than the one in
production, on the same evaluation set. Let's write this as a rule: if
the candidate beats the one in production by at least `min_gain`, the
alias moves to it.

```python
def should_promote(candidate, current, min_gain=0.003):
    gain = candidate["accuracy"] - current["accuracy"]
    return gain >= min_gain, round(gain, 3)


def try_promote(name, version):
    entry = read_registry()[name]
    current = entry["versions"][entry["aliases"]["production"] - 1]
    candidate = entry["versions"][version - 1]
    ok, gain = should_promote(candidate["metrics"], current["metrics"])
    if ok:
        set_alias(name, "production", version)
    result = "promoted" if ok else "kept out"
    print(f"version {version}: gain {gain:+.3f} -> {result}")


model_2, accuracy_2 = train("forest", make_customers(2000))
v2 = register("churn", model_2, {"accuracy": accuracy_2}, "forest")
try_promote("churn", v2)
model_3, accuracy_3 = train("logistic", make_customers(5000))
v3 = register("churn", model_3, {"accuracy": accuracy_3}, "more data")
try_promote("churn", v3)
print("production is version", read_registry()["churn"]["aliases"]["production"])
```

```text
version 2: gain -0.027 -> kept out
version 3: gain +0.005 -> promoted
production is version 3
```

Version 2 (a random forest without limits) was worse than the one in
production and was kept out. It still stays in the registry: the
information about what was tried and why it didn't pass isn't lost.
Version 3 (the same model, with more data) beat the one in production
and the alias moved to it.

Why is there a `min_gain`? As you saw in the Experiment Tracking section,
part of a small difference measured on a single set is luck. Replacing
the model in production for a very small lead can mean taking a risk for
nothing. The threshold is chosen by the domain; here it is 0.003, that
is, 3 correct predictions out of 1000 customers.

## Rolling back

Version 3 went into production. The next day the team that prepares the
data reports that part of the 5000-customer data was processed wrongly.
What do we do? Training a new model can take hours. But the old version
is in the registry:

```python
set_alias("churn", "production", 1)
entry = read_registry()["churn"]
print("production is version", entry["aliases"]["production"])
for alias, version in entry["history"]:
    print(f"{alias} -> version {version}")
```

```text
production is version 1
production -> version 1
production -> version 3
production -> version 1
```

A **rollback** took as long as pointing an alias at an old version. It
is the same idea as the deployment strategies in the CI/CD and DevOps
module: if the old version is standing by, a mistake is cheap. The only
condition is that the old versions' files are **not deleted**.

## The model card

The registry keeps the information a machine reads: version, file,
measurement. A description for people to read is needed too: a **model
card**. A short document; it says what the model is for, what it was
trained on, how it was measured and **where it should not be used**:

- **What it does:** predicts the customers who will cancel their
  subscription.
- **Who uses it:** the customer team, when deciding whom to call.
- **Data:** which version, how many customers, which months.
- **Measurement:** accuracy on the evaluation set, together with the
  baseline.
- **Limits:** only for this service's customers; not reliable if prices
  change a lot.

The limits part is the most skipped and the most important. A model
quietly goes wrong outside the world it was trained in; the card says so
from the start.

## Real tools

**MLflow**'s model registry does the same as what we wrote in this
section: when you register a model by name it gives a version number,
versions can carry aliases such as `production`, and the prediction code
loads the model from the address `models:/churn@production`. Pointing the
alias at another version changes the model in production.

## Summary

- A **model registry** keeps every model's numbered versions, their
  files' hashes, measurements and notes in one place.
- Version numbers **don't change** and are not reused.
- An **alias** says which version is in production; the prediction code
  asks for the alias, not the version number.
- A new version reaches production through a **gate**: on the same
  evaluation set it must beat the one in production by at least a
  threshold.
- A version that doesn't pass stays in the registry too.
- **Rolling back** is pointing the alias at an old version; old files
  are not deleted.
- A **model card** writes down what the model does, its data, its
  measurement and its limits in a form people read.
