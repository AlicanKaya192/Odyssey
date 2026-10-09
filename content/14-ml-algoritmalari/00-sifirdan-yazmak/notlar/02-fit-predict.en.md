Every model in this module is written with the same skeleton:

```python
class Model:
    def __init__(self, setting=1.0):
        self.setting = setting         # settings: the user's choice

    def fit(self, X, y):
        self.learned_ = ...            # what is learned: ends with _
        return self

    def predict(self, X):
        return ...                     # predict with learned_
```

## The contract's three rules

1. **Settings and what is learned are separate.** `__init__` only stores the
   settings (learning rate, tree depth). Everything that comes from the data is
   computed in `fit` and ends with `_`. So the question "is this number my
   choice or the data's?" can be read from its name.
2. **`fit` sees only the training data.** Computing a scaler's mean including
   the test data leaks information from test into training (**data
   leakage**); the model looks better than it really is. The right way:
   `fit(X_train)`, then `transform(X_train)` and `transform(X_test)`.
3. **`fit` returns `self`.** That is how the chain
   `Model().fit(X, y).predict(X_new)` works.

## Comparing with scikit-learn

The same routine in every section: our model and scikit-learn's are trained on
the same data, then compared with

- `np.allclose(ours, theirs)` for numerical results,
- `(ours == theirs).mean()` for labels (how many out of how many match),
- the same measure for performance (accuracy, mean squared error).

If there is a difference, it is usually a detail: `ddof`, how the
regularisation strength is scaled, which class is chosen on a tie, a random
start. Being able to explain the difference is a sign you understand the
model.
