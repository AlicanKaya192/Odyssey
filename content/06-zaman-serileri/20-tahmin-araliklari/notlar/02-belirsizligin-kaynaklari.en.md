There are four separate reasons a forecast goes wrong. The interval a model
gives usually counts only **one** of them.

## Four sources

| Source | What | Is it in the model's interval? |
|---|---|---|
| Noise | The unpredictable daily movement of the series | Yes |
| Coefficient uncertainty | The coefficients were estimated from limited data | Partly |
| Model uncertainty | The chosen model may be wrong or incomplete | No |
| The future changes | A new regime, an event not seen in training | No |

That is why intervals from a formula are almost always **too narrow** in
practice. The "95%" interval holding 87% in the lesson is a typical result.

An unknown external variable is a source too: if you filled the future
temperature with the seasonal normal (Section 18), the error of that estimate
should widen the sales interval. The model does not know this; it takes the
variable for a number known for certain.

## What widens an interval

- **A long horizon.** Errors accumulate.
- **Short training data.** The coefficients are unreliable.
- **A regime change.** Past errors do not represent the future.
- **Rare events.** The uncertainty of something that happens once a year
  cannot be measured from three observations.
- **A growing series.** The size of the error grows with the level; a
  percentage interval (a log model) is more honest than an absolute one.

## For an honest interval

1. Build the interval from **out-of-sample** errors (a rolling origin), not
   from the training residual.
2. Measure the coverage; if it does not hold, **scale**: enlarge the width of
   the "95%" interval until it would have covered 95% in the past.
3. Find the periods where coverage collapses; if a variable is missing, add
   it.
4. Re-measure regularly: as the series changes, so does the interval.

## A simple scaling

```python
ratio = np.abs(errors) / half_width           # |error| / half-width of the interval
factor = np.quantile(ratio, 0.95)             # the multiplier covering 95% of the past
calibrated_low = point - factor * half_width
calibrated_high = point + factor * half_width
```

`errors` and `half_width` are the errors in past experiments and the
half-width the model gave for those days. If `factor` is above 1 the model is
overconfident; you enlarge the interval by that much. You keep the **shape**
of the model (widening with the horizon) and correct its **size** by the data.

## Scenarios

An interval gives the uncertainty "if everything carries on as before". For
things that may not carry on as before, you build scenarios:

| Scenario | How |
|---|---|
| With / without the campaign | Run the external variable with two values (Section 18) |
| A cold winter / a mild winter | Two different proxies for the temperature |
| A new competitor | Lower the level by a percentage by hand |

A scenario carries no probability; it says "if this, then that". An interval
and a scenario do not replace each other; they are presented together.

## Misreadings

| What is said | The truth |
|---|---|
| "The actual value will be inside the interval." | With 95% probability. One in twenty is expected to fall outside |
| "The interval is narrow, so the forecast is good." | Narrow with low coverage is bad |
| "It fell outside, the model is broken." | One day says nothing; look at the rate |
| "95% is always better than 80%." | Wider, and less informative. Choose by the decision |
| "The middle of the interval is the most likely value." | Not with a skewed distribution (a log model) |

## Confidence interval and prediction interval

The two get mixed up:

- A **confidence interval** is the uncertainty of a **coefficient** or a mean:
  "the campaign effect is between 46 and 52". It narrows as data grows.
- A **prediction interval** is the uncertainty of a future **observation**:
  "tomorrow's sales are between 267 and 319". However much data there is, it
  stays as wide as the noise.

Although the statsmodels method is called `conf_int`, what it returns when
called on `get_forecast` is a prediction interval.
