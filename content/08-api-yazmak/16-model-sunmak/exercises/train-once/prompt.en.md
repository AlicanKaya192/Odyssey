`train_model()` is ready: it trains a model on the iris data and increases
`stats["trainings"]`. (In reality this would be `joblib.load`; in the
exercise we train instead of using a file, it takes 0.05 s.)

**What to do:**

1. `lifespan`: at startup `ml["model"] = train_model()` (**once**), at
   shutdown `ml.clear()`.
2. `GET /model` → `{"type": "LogisticRegression", "features": 4, "classes": [...]}`
3. `GET /stats` → `stats`; `{"trainings": 1}` even after several requests.
