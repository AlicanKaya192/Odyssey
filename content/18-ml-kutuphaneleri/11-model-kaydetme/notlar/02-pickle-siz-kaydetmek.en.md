A linear model is just a few numbers: the scaler's means and spreads, the
coefficients and the constant term. Writing them to a plain JSON file removes
two problems of `pickle` at once: the file cannot run code, and it does not
depend on the scikit-learn version.

```python
import json
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=500, n_features=4, n_informative=3,
                           n_redundant=0, random_state=2)
model = make_pipeline(StandardScaler(), LogisticRegression()).fit(X, y)
scaler, clf = model[0], model[-1]
params = {"mean": scaler.mean_.tolist(), "scale": scaler.scale_.tolist(),
          "coef": clf.coef_[0].tolist(), "intercept": float(clf.intercept_[0])}
text = json.dumps(params)
print(len(text))
p = json.loads(text)
z = (X - np.array(p["mean"])) / np.array(p["scale"])
proba = 1 / (1 + np.exp(-(z @ np.array(p["coef"]) + p["intercept"])))
print(bool(np.allclose(proba, model.predict_proba(X)[:, 1])))
```

```text
313
True
```

## What we see

- The whole model is a text of a few hundred characters.
- We computed the prediction ourselves with NumPy: scale, multiply by the
  coefficients, add the constant, sigmoid. The result equals scikit-learn's
  `predict_proba`.
- This file can be read in any language; predictions can be made without
  installing scikit-learn.

## Its limit

- It is practical only for models with a simple formula (linear, logistic).
  Writing a forest by hand means thousands of nodes.
- There are language-independent formats for complex models (like ONNX);
  they need extra packages, so they are not covered here.
