A residual is the error of a single record: `actual - predicted`. Measures
reduce those numbers to one; the residuals themselves show you **where** the
model goes wrong.

## Computing them

```python
residuals = y_test - prediction        # directly, for a pandas Series
residuals = [a - p for a, p in zip(y_test, prediction)]
```

| Sign | What it means |
|---|---|
| Positive | The model predicted **too low**; the actual value is higher |
| Negative | The model predicted **too high** |
| Near zero | A hit |

## What to look at

| What you look at | What it tells you |
|---|---|
| The largest absolute residuals | Where the model fails worst |
| The positive/negative balance | Whether there is a systematic bias |
| Residual against prediction | Whether error size grows with the prediction |
| Residual against a feature | Whether the model missed a relationship |
| The spread of residuals | A few outliers, or a general scatter |

## Four typical patterns

**1. Random scatter (what you want)**

Residuals around zero with no direction. The model caught what there was to
catch; the rest is noise.

**2. A sloped pattern**

As a feature grows, the residuals drift one way. **The model either does not
see that feature at all, or cannot capture its non-linear relationship.**

The fix: add the missing column, or move to a model that captures curves.

**3. A funnel (fan) shape**

As the prediction grows, so do the residuals. Off by 5 units on small
houses, by 50 on large ones.

The error is **proportional**, not absolute. Modelling the logarithm of the
target, or moving to MAPE, is the fix.

**4. A curved (U or inverted U) pattern**

Residuals lean one way in the middle and the other way at the ends. **The
relationship is not linear** and the model is trying to draw a straight
line.

The fix: add a squared term, or move to a tree-based model.

## Drawing the plot

```python
import matplotlib.pyplot as plt

residuals = y_train - model.predict(X_train)

plt.scatter(train_ages, residuals)
plt.axhline(0, color="red")
plt.xlabel("age")
plt.ylabel("residual")
plt.savefig("chart.png")
```

`axhline(0)` puts the zero line in; a pattern can only be read against it.

What goes on the horizontal axis depends on the question you are asking:

- **The prediction** (`model.predict(...)`) → does the error size change
  with the prediction?
- **A feature** → is the model using that feature correctly?
- **A column not in the model** → should you add that column?

The last is the most useful: if the residuals show a pattern against a
column you have but did not include, adding it improves the model.

## Measuring it with a number

You can look for a pattern without drawing anything:

```python
correlation = residuals.corr(df.loc[residuals.index, "age"])
```

A correlation near zero means no pattern. A number like `-0.937` means a
strong, directional relationship: as age goes up the model predicts too
high.

## Two warnings

**The mean of the residuals is not a measure of success.** For linear
regression it always comes out very close to zero on the training data — a
consequence of the method, not an achievement of the model. You look at the
**spread**, not the mean.

**Residual analysis may be done on the training data.** This does not
contradict the "never measure on training" rule: what happens there is
**diagnosis**, not measurement. The test set is set aside for measuring and
stays that way.

You can look at the test residuals too, but there are two limits: with few
records a pattern is hard to see, and the more you look at the test set the
more you spend it.

## What you do with a residual

Finding a pattern is not bad news but a **road map**:

| What you see | What to do |
|---|---|
| A slope against a column | Add that column to the model |
| A funnel | Transform the target or move to a proportional measure |
| A curved pattern | Try a non-linear model |
| A few extreme residuals | Look at those records one by one; they may be data errors |
| No pattern | The model has extracted what this data allows |

The last row is a result too: if you want more, you need new **data**, not a
new model.
