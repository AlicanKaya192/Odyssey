Data leakage is a model seeing, during training, information it will **not
have** at prediction time. The result is always the same: the test score
comes out higher than it should and the model is not that good in the real
world.

The worst part is how quiet it is. No error, no warning — just a number
prettier than expected.

## Four kinds of leak

### 1. Preparing before splitting

The most common one. Scaling, filling, encoding — every one of them learns
something from the data.

```python
scaler.fit_transform(X)                   # LEAKAGE: all the data
X_train, X_test = train_test_split(X)
```

The effect is usually small but real. The rule is not about the size of the
difference but about whether the measurement is honest.

### 2. Selecting features on all the data

This kind can be **large**.

```python
correlations = X.apply(lambda c: abs(c.corr(y)))    # LEAKAGE
best = correlations.nlargest(5).index
```

Picking the columns most correlated with the target by looking at all the
data means picking the ones that happen to agree with the test set.

Measured: 80 rows, 300 columns, **every value random** (no relationship with
the target at all). Leaky selection gives R² **0.442** — it makes a
non-existent model look real. Done correctly, R² comes out **-0.273**, which
says "there is nothing to learn here."

### 3. Mixing up time

Leaking the future into the past.

- Splitting a time series at random: showing the model tomorrow and asking
  it to predict yesterday.
- Using a column computed after the fact, like "total number of orders".
- Taking a mean over the whole period and writing it onto past rows.

With time data the split is made **by date**: the past for training, the
future for testing. `shuffle=False` is needed.

### 4. A column that carries the target

A column that hands over the answer.

| Column | Why it leaks |
|---|---|
| Predicting illness from "admission date" | Admission happens after diagnosis |
| Predicting cancellation from "cancellation reason" | The reason is written only once it is cancelled |
| Predicting a purchase from "total paid" | The payment is the purchase |
| Any column derived from the target | A copy of the answer |

This kind is the easiest to catch: **when performance is far higher than
expected, look here first.**

## The checklist

Before building a model, ask of every column:

1. **Will I have this column at prediction time?**
   If not, remove it.
2. **Does this column come into existence after the target?**
   If so, remove it.
3. **Could this column be derived from the target?**
   If in doubt, look at the correlation; a number like 0.99 is an alarm.

After building the model, ask:

4. **Is the result far better than expected?**
   R² 0.99, accuracy 100% — usually a sign of leakage, not success.
5. **Was every preparation step done after the split?**
   Scaling, filling, encoding, feature selection.
6. **Did I choose settings by looking at the test set?**
   If so, the test score is not honest.

## Preventing leakage structurally

Doing preparation by hand makes forgetting a step easy. `Pipeline` gathers
every step together with the model into one object:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", KNeighborsRegressor()),
])

pipe.fit(X_train, y_train)
pipe.predict(X_test)
```

`pipe.fit` learns the scaler **on training only**, and `pipe.predict`
applies what was learned. Leaking now takes deliberate effort.

That is section 11; here it is enough to know the solution exists.

## Signs to be suspicious of

| Sign | What to think |
|---|---|
| R² above 0.99 | Probably leakage |
| Accuracy 100% | Almost certainly leakage |
| One feature's importance is overwhelming | That column may carry the answer |
| The test score is higher than the training score | Something somewhere is wrong |
| Performance collapses in real use | The leak was already there |

The last row is the most expensive: the leak only surfaces once the model is
in use, and by then the trust is gone too.
