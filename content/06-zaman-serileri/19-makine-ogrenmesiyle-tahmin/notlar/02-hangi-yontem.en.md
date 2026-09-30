The model sections of the track end here. You have seen four families; this
gathers in one place when each of them is useful.

## Four families

| | Baselines | Exponential smoothing | ARIMA | Machine learning |
|---|---|---|---|---|
| Section | 14 | 16 | 17–18 | 19 |
| How it describes the series | Copies | Level, slope, season | Past values and surprises | A table of features |
| Data needed | One season | Two seasons | 50–100 observations | Hundreds to thousands of rows |
| External variables | None | None | Yes (`exog`) | Yes, many |
| More than one season | No | No | Through Fourier terms | Through features |
| Many series | One per series | One per series | One per series | A single model |
| Interpretability | Full | High | Medium | Low to medium |
| Maintenance | None | Little | Medium | A lot |

## The results in this track

Daily shop sales, 13 experiments, a 28-day horizon:

| Method | MAE |
|---|---|
| Seasonal naive | 17.95 |
| Holt–Winters | 15.91 |
| ARIMA | 15.94 |
| Direct gradient boosting + calendar | 13.80 |
| Direct linear + calendar | 10.64 |
| ARIMA + calendar | 10.23 |

Three steps show: copying (18), modelling the series (16), knowing the
calendar (10). Each step was climbed by a piece of **information**, not by a
model.

## The order of decisions

```text
1. The table of baselines                            -> the bar
2. A marked trend / season in the series?            -> exponential smoothing
3. Short memory left in the residual?                -> ARIMA
4. Do the worst experiments gather in the calendar?  -> external variables
5. Many series, many variables, non-linear effects?  -> machine learning
6. At every step: the same rig, against the bar
```

If a step brings no gain, stop there. Of two methods that tie, choose the
simpler one.

## Combining

The **average** of the forecasts of different methods is often better than
each of them alone: while one misses high the other misses low, and the errors
partly cancel.

```python
combined = (forecast_hw + forecast_arima + forecast_ml) / 3
```

The condition: the methods must be really **different** (averaging two models
that make the same error with the same information gains nothing) and none of
them may be very poor. Choose the weights on validation, not on the test.

## Three rules for trees

1. **Forecast the change, not the level.** The target is a difference or a
   ratio.
2. **A small model for little data.** Shallow trees, strong regularisation; do
   early stopping with a validation part split by time.
3. **Keep the number of features in line with the number of rows.** Fifty
   features on a thousand rows is an invitation to memorise.

## Frequently asked

**Deep learning?** Strong when there are many long series and a lot of data.
On a single short series it rarely beats the methods of this track, and it is
expensive to maintain. The same rig and the same bar apply.

**Ready-made automatic tools?** There are libraries that choose the order, the
components or the features by themselves. Inside them the steps of this track
are running; if you know what they do you can check their results. Do not use
them unchecked.

**The model keeps getting worse.** The data has changed (Section 21). Refit
regularly, watch the skill, and raise an alarm when it drops below the
baseline.
