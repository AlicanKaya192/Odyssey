A model rarely works alone: first the data is scaled, encoded, gaps are
filled. When serving, **all** these steps must be the same as in training.

## Forgetting the scaler (measured)

In training we scaled the data with `StandardScaler` and trained a k-NN
model; when serving we used only the model and gave it raw measurements:

```text
flower                raw input   scaled input
5.1, 3.5, 1.4, 0.2    2           0
5.9, 3.0, 4.2, 1.5    2           1
6.7, 3.0, 5.2, 2.3    2           2
```

With raw input the model said `2` (virginica) for **all** 150 flowers:
accuracy fell from 0.953 to 0.333. No error, no warning. This is the most
dangerous kind of bug in an API: everything seems to work.

## The fix: saving the whole pipeline

Remember the Pipeline section of the ML track:

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

pipe = make_pipeline(StandardScaler(), KNeighborsClassifier())
pipe.fit(iris.data, iris.target)
joblib.dump(pipe, "model.joblib")
```

When serving, `joblib.load("model.joblib").predict(row)` takes the raw input,
scales it first and then predicts (we measured: `6.7, 3.0, 5.2, 2.3` → `2`).
The API doesn't need to know about scaling; it's inside the pipeline.

## The rule

**Everything that was `fit` in training is saved in the same file.** Saving
the scaler separately from the model, or rewriting the scaling by hand in
the API, will drift apart one day.

## Version compatibility

A model saved with `joblib` should be loaded with the scikit-learn version
that saved it. A different version may give a warning or an error. That's
why the version is pinned in `requirements.txt` (`scikit-learn==...`); the
Docker image is built with the same version too.
