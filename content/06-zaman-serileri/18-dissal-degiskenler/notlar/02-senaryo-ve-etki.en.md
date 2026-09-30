A model with external variables does not only forecast; it answers two more
questions: "how much did this event matter?" and "what if we do that?"

## The recipe

1. **List the variables** and ask of each: is it ready at forecast time?
2. **Build the table:** `X_train` for training, `X_future` for the future. The
   same columns, the same order, no `NaN`.
3. **Test the model without variables first** (the bar).
4. **Add the variables** and look at the coefficients: are the sign and the
   size sensible?
5. **Test with a rolling origin**; in every experiment fill the unknown
   variable with what is known at that moment.
6. **Report the ceiling separately:** the result with the actual values.

## The future table

```python
future_index = pd.date_range(train.index[-1], periods=h + 1, freq="D")[1:]
future = pd.DataFrame(index=future_index)

future["promo"] = future_index.isin(planned_promo_days).astype(int)
future["holiday"] = future_index.isin(holiday_dates).astype(int)

normal = train["temp_c"].groupby(train.index.dayofyear).mean()
future["temp_c"] = [normal.get(day, normal.mean()) for day in future_index.dayofyear]

forecast = fit.forecast(h, exog=future[columns])
```

`normal.get(day, normal.mean())`: for a day not in the training data, such as
day 366 of a leap year, it falls back to the mean.

## Checking a coefficient

| Question | Where to look |
|---|---|
| Is the sign what I expected? | `coef` |
| Can it be told from zero? | The p-value and the confidence interval |
| Is the size reasonable? | Compare with a rough calculation (neighbours on the same weekday) |
| Is it stable? | Refit on different training periods |
| Is it mixed up with another variable? | Remove one and look at the other's coefficient |

A coefficient with an unexpected sign usually points to a **confounder**. If
"the campaign lowers sales" comes out, the campaigns are probably run in weak
periods anyway and the model does not see that weakness.

## Asking a scenario

```python
with_promo = future[columns].copy()
without_promo = with_promo.copy()
without_promo["promo"] = 0

gain = fit.forecast(h, exog=with_promo) - fit.forecast(h, exog=without_promo)
print(round(gain.sum()))
```

This is the total extra sales the model attributes to the campaign. Two
warnings:

- The model only knows campaigns **of the kind it saw in training**. For a
  length or a discount rate never tried, what it says is an extrapolation.
- A coefficient is an **association**; a causal claim requires knowing how the
  campaign days were chosen. If campaigns were put on random days the
  coefficient is reliable; if always on good days, it is inflated.

## The effect of a past event

For "how much did the campaign on 14 March bring?" you need a forecast of what
would have happened **had the event not occurred**:

1. Fit the model on the data before the event.
2. Forecast the event day with `promo = 0`.
3. Actual − forecast is the effect of the event (plus forecast error).

In Section 13 you repaired outlier days "with the average of a week before and
a week after"; that was the rough, model-free answer to the same question.

## Where does the error of an unknown variable go?

```text
error of the sales forecast  =  the model's own error
                              +  coefficient x (forecast error of the variable)
```

In the café the temperature coefficient is 5.5. If the seasonal normal misses
the temperature by 2.2 degrees on average, that brings 5.5 × 2.2 ≈ 12 units of
extra uncertainty to the sales forecast. The gap between the ceiling and the
real result (9.4 and 15.0) is exactly this.

The conclusion: adding an unknown variable pays only if its **predictable**
part is large. The seasonal part of temperature is predictable; its daily
movement cannot be foreseen 28 days ahead.

## Is a variable worth adding?

On the same rolling origin, with and without the variable:

| Case | Decision |
|---|---|
| The error falls clearly, in most experiments | Add it |
| It falls only "with the actual value" | The variable is good but its future is unknown; look for a better proxy |
| The error does not change | Do not add it; maintenance is a cost |
| The mean falls, the worst experiment grows | Careful: the variable misleads in some periods |

## Maintenance

- The list of holidays and the campaign calendar are **updated every year**; a
  missing holiday means the model takes that day for an ordinary one.
- If a new kind of event has appeared (a new discount day), it is not in the
  model in its first year; a manual correction or the coefficient of a similar
  event is needed.
- Re-estimate and watch the coefficients from time to time: a drifting
  coefficient says the effect is changing.
