## The four settings of the rig

| Setting | Question | Typical choice |
|---|---|---|
| Horizon (`h`) | How many steps ahead will I really forecast? | The horizon of the decision: 7, 28, 12 |
| Step (`step`) | How many steps between origins? | `h` (non-overlapping tests) or one season |
| Number of experiments | How many origins? | At least 5–10; covering a full year if possible |
| Window | How far back should the training go? | Expanding; sliding if the series is changing |

Before the first origin there must be enough data for the model to learn from:
at least two full seasons.

## A general function

```python
import numpy as np
import pandas as pd


def backtest(y, forecast, first, step, h, count, window=None):
    rows = []
    for i in range(count):
        cut = pd.Timestamp(first) + step * i * y.index.freq
        train = y.loc[:cut]
        if window is not None:
            train = train.iloc[-window:]
        test = y.loc[cut:].iloc[1:h + 1]
        if len(test) < h:
            break
        predicted = np.asarray(forecast(train, h), dtype=float)
        rows.append({
            "cut": cut,
            "mae": np.mean(np.abs(test.to_numpy() - predicted)),
            "bias": np.mean(test.to_numpy() - predicted),
        })
    return pd.DataFrame(rows).set_index("cut")
```

- `step * i * y.index.freq` works at any frequency (daily, monthly); the
  series must be regular, via `asfreq`.
- `window=None` is an expanding window; a number makes it a sliding one.
- `forecast(train, h)` sees only `train`. Every calculation, a seasonal
  factor, a mean, filling, must be done **inside that function**.

Usage:

```python
table = backtest(s, snaive, "2024-01-02", step=28, h=28, count=13)
print(table["mae"].agg(["mean", "std", "min", "max"]).round(2))
```

## Overlapping and non-overlapping tests

| | Non-overlapping (`step = h`) | Overlapping (`step < h`) |
|---|---|---|
| Number of experiments | Few | Many |
| Are the experiments independent | Largely | No: the same days are in many tests |
| When | With plenty of data | With short data; when error by horizon is wanted |

With overlapping tests the mean looks more stable, but since the experiments
are not independent of each other the standard deviation **understates** the
real uncertainty.

## What to report

```python
table["mae"].mean()             # typical performance
table["mae"].std()              # variation from period to period
table["mae"].max()              # the worst period
table["mae"].idxmax()           # when
table["bias"].mean()            # systematic drift
```

Look at **when** the worst experiment was: if it is always the same season
(year end, a holiday week) the model does not know that period, and the fix is
a calendar variable (Section 18), not a more complex model.

## Comparing two methods

The same origins, the same horizon, the same measure. Then look at the
difference experiment by experiment:

```python
diff = table_a["mae"] - table_b["mae"]
print(round(diff.mean(), 2), round(diff.std(), 2), int((diff < 0).sum()), len(diff))
```

- If the mean of the difference is small next to its standard deviation: a
  tie.
- If A wins in about half the experiments: a tie.
- If A wins in nearly all the experiments and the gap is worth having: A is
  better.

Of two methods that tie, choose **the simpler one**.

## Validation and test

```text
|---------- training ----------|-- validation experiments --|-- test experiments --|
                                 settings are chosen here     once, at the very end
```

- All the trials of settings happen on the validation experiments.
- The test experiments are looked at last, for **a single** candidate.
- If you changed a setting after seeing the test result, you need a new test
  period.
- For final use the model is refitted on **all the data**, validation and test
  included.

## `TimeSeriesSplit`

```python
from sklearn.model_selection import TimeSeriesSplit

splitter = TimeSeriesSplit(n_splits=5, test_size=28, gap=0, max_train_size=None)
```

| Argument | Meaning |
|---|---|
| `n_splits` | The number of experiments |
| `test_size` | The length of each test (the horizon) |
| `gap` | The number of rows skipped between the end of training and the start of the test |
| `max_train_size` | If given, a sliding window; if not, an expanding one |

What is `gap` for? If the features of a model forecasting 7 days ahead include
yesterday's value, the 6 days before the test day are not known at forecast
time. `gap=6` removes those days from both training and test.

It returns row **positions**, not dates: `s.iloc[train_idx]`. The series must
be sorted and regularly spaced.

## Signs of leakage

- The test error is **smaller** than the training error.
- The multi-step error is almost the same as the one-step error.
- A complex model beats the baseline by an unbelievable margin (skill > 0.8).
- The error multiplies the moment you go to real use.

If you see one, trace the rig line by line: the date of every number going
into the `forecast` function must not be later than `cut`.
