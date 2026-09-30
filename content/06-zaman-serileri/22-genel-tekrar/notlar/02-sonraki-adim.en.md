This track taught forecasting a single series soundly. From here you can go
three ways: deeper, wider, or into a real job.

## First: repeat it with your own data

The quickest way to learn is to run the flow from start to finish on a series
**you chose yourself**. Open, long series:

| Source | What is there |
|---|---|
| National statistics offices (TurkStat, Eurostat) | Monthly inflation, unemployment, production, tourism |
| Central banks | Exchange rates, interest rates, money supply |
| Weather archives | Hourly / daily temperature, rainfall |
| City open data portals | Public transport, traffic, bikes, energy |
| Your own data | Step counts, spending, sleep: small, but yours |

The same eight steps on every series: raw data → regular series → diagnosis →
baseline → rig → model → interval → monitoring. Finishing one series teaches
more than starting ten.

## Deeper: more of the same subject

| Topic | What it adds | Where to start |
|---|---|---|
| State space models, the Kalman filter | Models that work naturally with missing data and whose components change over time | `statsmodels.tsa.statespace`, `UnobservedComponents` |
| The ETS family | The version of exponential smoothing that gives intervals and is chosen automatically | `statsmodels` `ETSModel` |
| Automatic model selection | Not searching `(p, d, q)` by hand | `pmdarima`, `statsforecast` |
| Multiple seasonality | Daily + weekly + yearly in hourly data | `MSTL`, TBATS, Fourier |
| Change point methods | Finding many breaks together | `ruptures` |
| Probabilistic forecasting | A whole distribution instead of one interval; the CRPS measure | Quantile regression, conformal intervals |

## Wider: what is not in this track

| Topic | The question it answers |
|---|---|
| Global models | Forecasting a thousand series with one model; short series learn from each other |
| Hierarchical forecasting | Making shop, city and country forecasts add up |
| VAR, cointegration | Series that affect each other (interest and exchange rates) |
| GARCH | Changing volatility in financial series |
| Intermittent demand | Series that are zero on most days (spare parts); Croston's method |
| Deep learning | Very long, very many series; N-BEATS, temporal transformers |
| Causal impact | "What would have happened without the campaign?": interrupted time series, synthetic control |

Libraries: `statsforecast` (fast classical models), `sktime` and `darts` (many
methods behind one interface), `prophet` (business series heavy with calendar
effects). None of them comes with the app; you install them in your own
environment (the Packages and Environments section).

Whichever you use, the rig of this track does not change: a baseline, a
rolling origin, the worst experiment, the residual. If a new method cannot
beat seasonal naive across 13 experiments, it has not beaten it, however
shiny its name.

## What is different in a real job

- **Data arrives late and gets revised.** Yesterday's number changes tomorrow.
  Keep what you had in hand **on the day** you made the forecast; otherwise
  tests in hindsight are run with information that did not exist.
- **A forecast is for a decision.** Not "what is the MAE?" but "which decision
  will be made with this forecast, and what does being wrong cost?" decides
  the method and the measure.
- **The simple model survives.** A model that runs every night, that you can
  tell is broken, that is explained in a sentence, is worth more than one that
  is 2% better and that nobody understands.
- **People intervene in the forecast.** The sales team adjusts the number by
  hand. Keep both versions and measure which is better.
- **The series disturbs itself.** If stock is raised on the strength of the
  forecast, sales change too; the model starts forecasting a world it affects.

## Next in Odyssey

This track shares its ground with the Machine Learning track: the feature
table, validation, leakage. If you have not finished that, go there; if you
have, read Section 19 once more, the two complete each other. The probability
and statistics sections of the Mathematics track give the reasoning behind the
intervals and the tests.
