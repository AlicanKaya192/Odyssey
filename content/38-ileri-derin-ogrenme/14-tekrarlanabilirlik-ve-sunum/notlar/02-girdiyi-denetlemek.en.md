The prediction function in the lesson checked only the length. Input from
the real world is much more creative: text, missing values, `NaN`, nested
lists. A check placed in front of the model names the error "the input was
wrong" instead of "the model talked nonsense".

```python
import math


def check_features(values, n=6):
    if not isinstance(values, list) or len(values) != n:
        return f"expected a list of {n} numbers"
    if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in values):
        return "values must be finite numbers"
    return None


for v in ([1, 2, 3, 4, 5, 6], [1, 2], [1, 2, 3, 4, 5, float("nan")], "abc"):
    print(check_features(v))
```

```text
None
expected a list of 6 numbers
values must be finite numbers
expected a list of 6 numbers
```

- `None`: the input is valid. The others are clear messages that can be shown
  to the user.
- `math.isfinite` catches both `NaN` and infinity; a `NaN` passing through a
  network turns the whole output into `NaN`, and `argmax` silently picks a
  class.
- Careful: in Python `True` is an `int`, so `[True, ...]` passes this check.
  If needed, reject `type(v) is bool` separately.

## What else when serving?

- **The same preprocessing:** if you scaled the data in training (mean,
  standard deviation), the same numbers are stored with the model and applied
  at prediction time too. This is the most common serving mistake: the model
  is right, the input is on a different scale.
- **Version:** add the model's version to the answer
  (`{"label": ..., "model": "1.2"}`); when a complaint arrives, you know which
  model answered.
- **Batch requests:** accepting several rows in one call is much faster than
  calling row by row (the measurement in the Performance section).
- **Logging:** keep part of the incoming inputs and answers; only this way can
  you tell whether the data the model sees drifts over time (data drift).
