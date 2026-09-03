# Regression Metrics

The previous section produced `18.5` and we called it good by looking at the
baseline. That was right, but incomplete.

Because `18.5` is a **summary**. Behind the summary sit ten predictions, and
how those predictions are spread says more than their average. This section
looks behind it.

## It all starts with the residual

The error of one prediction is the difference between the actual value and
the prediction. It is called the **residual**.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">residual</span><span class="anat-body"><code>actual - predicted</code> — the error of a single record</span></div>
    <div class="anat-row"><span class="anat-label">positive</span><span class="anat-body">the model predicted <b>too low</b>; the actual value came out higher</span></div>
    <div class="anat-row"><span class="anat-label">negative</span><span class="anat-body">the model predicted <b>too high</b></span></div>
  </div>
  <figcaption>Every regression measure is derived from these numbers. What separates them is how they add the residuals up.</figcaption>
</figure>

Say the residuals of eight predictions are these:

```
[12, -7, -15, 15, -15, 30, -8, 10]
```

There is more than one way to **reduce those eight numbers to one**, and
each way cares about something different.

## MAE — mean absolute error

The most direct way: drop the signs and take the average.

```python
mae = sum(abs(e) for e in errors) / len(errors)   # 14.0
```

**Why the absolute value:** with the signs kept, +15 and -15 cancel out and
the model looks perfect. The absolute value measures the **size** of the
mistake, not its direction.

MAE's greatest strength is readability: its unit is the target's unit. You
can say "I am off by 14 thousand on average" and everyone understands.

```python
from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(y_test, prediction)
```

## MSE and RMSE — squaring instead

The second way: square the residual instead of taking its absolute value.

```python
mse = sum(e ** 2 for e in errors) / len(errors)   # 241.5
rmse = mse ** 0.5                                 # 15.54
```

Squaring also removes the sign, but it has a side effect: **large errors
gain disproportionate weight.** An error of 30 is punished nine times as
hard as an error of 10.

MSE's unit is the target's unit squared — there is no such thing as "241.5
thousand squared". So its square root is taken: **RMSE** is back in the
target's unit.

## The same MAE, very different RMSE

The example that shows the difference best is this one. Two models, and the
actual value is 100 every time:

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Model A</h4>
      <p>Off by <b>10</b> on every prediction.<br>MAE <b>10.0</b> · RMSE <b>10.0</b></p>
    </div>
    <div class="versus-side">
      <h4>Model B</h4>
      <p>Gets nine exactly right, misses one by <b>100</b>.<br>MAE <b>10.0</b> · RMSE <b>31.62</b></p>
    </div>
  </div>
  <figcaption>MAE cannot tell them apart. RMSE sees B's single large error and punishes it three times as hard.</figcaption>
</figure>

**Which is the better model?** The answer is not in the measure but in the
problem.

- For a delivery-time estimate, being ten minutes out is tolerable; but
  being 100 minutes out on a single delivery loses the customer.
  **B is bad, RMSE is right.**
- For a total cost estimate, small deviations accumulate while one large
  deviation dissolves into the average. **A is bad, MAE is right.**

**The problem chooses the measure, not habit.** The answer to "which measure
should I use" is the answer to "is one large error more expensive than the
sum of several small ones".

## R² — the unitless one

MAE and RMSE speak in the target's unit. That is readable, but it creates a
problem: **numbers from two different problems cannot be compared.** MAE 18.5
for house prices, MAE 2.1 for temperatures — which is the better result?

R² solves that, because it has no unit:

```
R² = 1 - (the model's error) / (the baseline's error)
```

Spelled out:

```python
mean = y_test.mean()
ss_res = sum((a - p) ** 2 for a, p in zip(y_test, prediction))
ss_tot = sum((a - mean) ** 2 for a in y_test)
r2 = 1 - ss_res / ss_tot        # 0.943
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">R² = 1</span><span class="anat-body">perfect; no error at all</span></div>
    <div class="anat-row"><span class="anat-label">R² = 0.94</span><span class="anat-body">only 6% of the baseline's error is left</span></div>
    <div class="anat-row"><span class="anat-label">R² = 0</span><span class="anat-body">as good as the baseline; nothing was learned</span></div>
    <div class="anat-row"><span class="anat-label">R² &lt; 0</span><span class="anat-body"><b>worse</b> than the baseline; the model gets discarded</span></div>
  </div>
  <figcaption>R²'s zero point is the baseline. The previous section's baseline is built into this measure.</figcaption>
</figure>

**Watch out:** R²'s zero point is **the test set's own mean**. That differs
slightly from the baseline you built by hand — you used the training mean.
The two numbers come out close, but they are not the same.

**Be careful with "R² explains x percent".** A common but loose phrase. R²
0.94 can be read as "I explained 94% of the variation in the target"; but
this is not an **explanation**, it is a measure of fit. The model does not
know what it explained or why.

## MAPE — speaking in percentages

One more measure: express the error as a share of the actual value.

```python
mape = sum(abs((a - p) / a) for a, p in zip(actual, predicted)) / len(actual)
```

Understandable: "I am off by 8% on average". But it has two traps:

- **A zero actual value blows up the division.** If a sales forecast has a
  day with zero sales, MAPE cannot be computed.
- **It is not symmetric.** Saying 50 instead of 100 is a 50% error; saying
  150 instead of 100 is also 50%. But saying 200 instead of 100 is 100%, and
  saying 0 instead of 100 is also 100%. The penalty for predicting low is
  capped; the penalty for predicting high is not. A model notices this and
  drifts towards **systematically predicting low**.

It gets used, but not blindly.

## Looking at the residuals: this is the real work

Measures give you a number. **The residuals themselves** show you where you
went wrong — and that is usually more useful.

Where did the previous section's single-feature model make its largest
error?

```
largest residual: 43.87
that house's area: 130
that house's age:  26
```

One of the oldest houses in the dataset. The model does not know about age —
we never gave it that column — and that is exactly where it fails.

That is a single record. But is it a **pattern**, or a coincidence?

## The residual plot

Plot the residuals against a column the model never saw, and this is what
comes out:

```
correlation between residual and age: -0.937
```

Almost a perfect relationship. As age goes up the model predicts
**systematically too high**.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Residuals with no pattern</h4>
      <p>Scattered randomly around zero.<br>The model caught what there was to catch; the rest is noise.</p>
    </div>
    <div class="versus-side">
      <h4>Residuals with a pattern</h4>
      <p>They lean in one direction.<br>The model <b>missed</b> something, and it is still there.</p>
    </div>
  </div>
  <figcaption>A residual plot is not an exam but a diagnosis: it shows what the model failed to learn.</figcaption>
</figure>

**Seeing a pattern in the residuals is good news.** A pattern means there is
still something learnable sitting there: here, adding the `age` column. When
we added it in the previous section the error dropped from 18.5 to 7.13 —
the residual plot was saying so **before** we added it.

**One detail:** the mean of a linear regression's residuals on the training
data always comes out very close to zero. That is not a sign of success but
a consequence of the method. You look at the **spread**, not the mean.

**Another detail:** residual analysis is usually done on the **training**
data, and that does not contradict the "never measure on training" rule.
You are not measuring there, you are **diagnosing**. The measurement is
still on the test set.

## What goes in a report

A single number is not a report. A regression result carries these:

| What | Why |
|---|---|
| MAE (or RMSE) | How far off you are, in an understandable unit |
| R² | A comparable ratio |
| The same measure for the baseline | The grounds for the word "good" |
| On what data, with how many records | The context the number is valid in |
| Where it goes wrong | The largest errors, the residual pattern |

The last row is the one most often skipped and often the most important. A
model whose errors all fall on one customer segment is unusable, however
good its average.

## None of this works for classification

This whole section was about a **numeric target**. When the target is a
category there is no such thing as a residual: the difference between "cat"
and "dog" is not a number.

There the measures are entirely different — accuracy, precision, recall —
and that is exactly what the next section is about.
