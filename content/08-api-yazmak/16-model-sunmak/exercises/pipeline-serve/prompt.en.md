This API gives no error, but it says the same species for every flower: the
model was trained on scaled data, while serving gives raw measurements.

**What to do:** change `train_model` so it trains the scaler and the model
as **one pipeline** (`make_pipeline(StandardScaler(), KNeighborsClassifier())`).
Don't touch the endpoint.

- `5.1, 3.5, 1.4, 0.2` → `setosa`
- `5.9, 3.0, 4.2, 1.5` → `versicolor`
- `6.7, 3.0, 5.2, 2.3` → `virginica`
