These terms will come up constantly for the rest of the track. They are the
ones you will see in library documentation and in error messages.

## Data

| Term | Meaning |
|---|---|
| Training data (train) | The past the model sees |
| Test data (test, holdout) | The last stretch kept back to compare with the forecast |
| Validation data | An intermediate stretch used when choosing models and settings; the test is kept for the very end |
| Origin | The last moment of the training data; when the forecast is made |
| Horizon (`h`) | How many steps ahead is forecast |
| Step | One unit of the frequency of the data: a day, a month |

## Kinds of forecast

| Term | Meaning |
|---|---|
| Point forecast | A single number: "310 tomorrow" |
| Prediction interval | A range and a probability: "280–340 with 95% probability" (Section 20) |
| One-step | Only the next step |
| Multi-step | Several steps from the same origin |
| In-sample | The fit of the model over the period it was trained on |
| Out-of-sample | The forecast over a period the model has not seen; this is the real measure |

An in-sample error is always optimistic: the model has already seen that data.
The success of a model is measured only by its **out-of-sample** error.

## Two routes to a multi-step forecast

**Recursive.** Forecast one step, treat that forecast as data and forecast the
next. Errors accumulate, but one model is enough. The weekly chain of seasonal
naive is its simplest form.

**Direct.** A separate rule or model for each horizon: one for "7 days ahead",
one for "14 days ahead". Errors do not accumulate, but many models are needed.
In Section 19 you will build both.

## Error

| Term | Definition | What it tells you |
|---|---|---|
| Error | actual − forecast | The deviation of a single step |
| Residual | actual − in-sample fit | The deviation of the model on the training data |
| MAE | The mean of the absolute errors | The typical deviation, in the unit of the series |
| Bias | The mean of the errors | A systematic drift and its direction |
| Skill | 1 − MAE / baseline MAE | The gain over the baseline |

The sign convention: **error = actual − forecast**. A positive error: the
forecast was too low. Some sources use the opposite; when reading a report,
check which one it is.

A residual and an error are not the same thing: a residual is on data the
model **has seen**, an error on data it **has not**. If the residuals are
small while the errors are large, the model has memorised.

## Leakage

Information that could not be known at forecast time reaching the model. The
most common routes in time series:

- Splitting training and test at random.
- Computing numbers such as a mean, a scale or a growth rate from all the
  data.
- A `center=True` window, `shift(-k)`, `interpolate`, `bfill`: all look into
  the future.
- Not putting `shift(1)` before `rolling`.
- Using an external variable not yet published at forecast time (Section 18).

The sign of leakage: a test error too good to believe. If a result is too
good, look for leakage first.

## Backtesting

Running the model from many different origins in the past and comparing its
forecast with the truth at each. Dozens of training/test splits instead of
one; the result depends far less on chance. The main subject of Section 15.

## Baseline (benchmark)

A simple forecast produced without learning anything: mean, naive, seasonal
naive, drift. The **bar** every model is compared with.
