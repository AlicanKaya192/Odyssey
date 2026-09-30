The two building blocks of the ARIMA of Section 17. Here we only build the
**intuition**: how each one carries a shock, and what it looks like in the
correlogram.

## The shock

Both are made of the same raw material: **white noise** `e`. An independent,
unpredictable surprise every day. AR and MA are two different rules for how
that surprise spreads into the following days.

## AR: the series remembers itself

$$y_t = \phi\, y_{t-1} + e_t$$

Today = `φ` times yesterday + today's shock. The trace of one shock with
`φ = 0.7`:

| Day | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Effect | 1 | 0.7 | 0.49 | 0.34 | 0.24 | 0.17 |

It never becomes exactly zero, but it shrinks every day. That is also the
shape of the ACF: $\rho_k = \phi^k$.

Examples: the temperature anomaly (if it is warm today it will probably be
warm tomorrow), a stock level, the number waiting in a queue. **The state
itself** is carried over.

The value of `φ`:

- Close to 0: a memory so short it hardly exists.
- Close to 1: a very long memory; shocks fade very slowly.
- Exactly 1: a random walk. A shock never fades; the series is not stationary.
- Negative: the series goes up and down in turn; the ACF decays changing sign.

## MA: the shock echoes

$$y_t = e_t + \theta\, e_{t-1}$$

Today = today's shock + `θ` times yesterday's shock. The trace of one shock
with `θ = 0.7`:

| Day | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Effect | 1 | 0.7 | 0 | 0 |

One day later it is still felt; two days later it is **completely** gone. The
ACF, too, cuts off after lag 1. The value at lag 1:

$$\rho_1 = \frac{\theta}{1 + \theta^2} = \frac{0.7}{1.49} = 0.47$$

Examples: the effect of a campaign spilling into the next day, a delivery
delay made up for the day after, the correction of a measurement error. **The
event itself** echoes; the state is not carried over.

## Generating and seeing

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
e = rng.normal(0, 1, 650)

ar = np.zeros(650)
for i in range(1, 650):
    ar[i] = 0.7 * ar[i - 1] + e[i]

ma = e[1:] + 0.7 * e[:-1]
```

Dropping the first 50 values is a good habit: the AR series starts from zero
and takes time to settle.

## Fingerprints

| Process | ACF | PACF |
|---|---|---|
| AR(1), `φ > 0` | Positive, exponential decay | A single bar at lag 1 |
| AR(1), `φ < 0` | Decay with changing sign | A single negative bar at lag 1 |
| AR(2) | Decay, or a decaying wave | Bars at the first two lags |
| MA(1), `θ > 0` | A single positive bar at lag 1 | Decay with changing sign |
| MA(1), `θ < 0` | A single negative bar at lag 1 | Negative, exponential decay |
| MA(2) | Bars at the first two lags | Decay |
| ARMA(1, 1) | Decay after lag 1 | Decay after lag 1 |

## Why mirror images?

- In AR, today is linked **directly only to yesterday** (one PACF bar), but
  since yesterday is linked to the day before, the chain goes on (a long ACF
  tail).
- In MA, today and two days ago share **no shock** (the ACF cuts off). But if
  you try to explain the series by its own past values you need many lags (a
  long PACF tail).

## A seasonal echo

The same two ideas hold at the length of the season. The seasonal difference of
the daily sales had a single negative bar at lag 7 (−0.41) and none at 14:
that is the fingerprint of a **seasonal MA(1)**. The surprise on the same day
last week affects this week; two weeks ago does not.

In Section 17 you will choose these four numbers: `p` (AR), `q` (MA), `P`
(seasonal AR), `Q` (seasonal MA). You will read all of them off the ACF and
PACF.

## Which one is "better"?

Both serve the same purpose: describing short-term memory with a few numbers.
The same series can often be described approximately by either (a long AR
resembles a short MA, and the other way round). The choice goes to the model
that turns the residual into white noise **with the fewest parameters**.
