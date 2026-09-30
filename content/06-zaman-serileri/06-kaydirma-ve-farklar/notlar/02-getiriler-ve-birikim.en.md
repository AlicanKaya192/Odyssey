## Simple returns and logarithmic returns

```python
r = close.pct_change()            # simple return
log_r = np.log(close).diff()      # logarithmic return
```

| | Simple return | Logarithmic return |
|---|---|---|
| Definition | `P1 / P0 - 1` | `ln(P1 / P0)` |
| Reading it | Directly a percentage | Very close to a percentage for small values |
| Building up over time | **Multiply**: `(1 + r).cumprod()` | **Add**: `log_r.cumsum()` |
| Symmetry | A 10% rise + a 10% fall ≠ 0 | +0.0953 and -0.0953 cancel exactly |
| When | Reporting, explaining to people | Modelling, statistics |

For small changes the two are almost the same: a 1% simple return is a
0.00995 log return. The gap widens as changes grow: a 50% rise is 0.405, a
50% fall -0.693.

## Why do they not add up?

| Day | Price | Simple return | Log return |
|---|---|---|---|
| 0 | 100 | — | — |
| 1 | 110 | +10% | +0.0953 |
| 2 | 99 | -10% | -0.1054 |
| Total | | 0% (wrong) | -0.0101 → -1.0% (right) |

The price went from 100 to 99: the real change is -1%. The sum of the simple
returns says zero. The second day's 10% is taken from a larger base (110), so
the two percentages are not the same size.

From a log return back to a simple one: `np.exp(total) - 1`.

## Cumulative return

```python
cumulative = (1 + r).cumprod() - 1            # each day, the return since the start
total = (1 + r).prod() - 1                    # a single number
same = close.iloc[-1] / close.iloc[0] - 1     # the same thing
```

## An index based at 100

The way to compare series at different levels on one chart is to start them
all from the same point:

```python
index = close / close.iloc[0] * 100
```

The first day is 100; a day reading 166.1 is 66.1% above the start. A stock
at 50 and one at 5000 can now be read side by side.

The base can be another date too: `close / close.loc["2024-01-02"] * 100`.
Which date you pick as the base changes the story the chart tells; justify
the choice.

## Compound annual growth

To summarise a change over several years as "how many percent a year on
average":

```python
years = (close.index[-1] - close.index[0]).days / 365.25
cagr = (close.iloc[-1] / close.iloc[0]) ** (1 / years) - 1
```

66% growth in three years is not 22% a year but about **18%**: each year's
growth sits on top of the previous one. Dividing the total by the number of
years ignores compounding.

## Drawdown

How far a series is below its highest point so far:

```python
peak = close.cummax()
drawdown = close / peak - 1          # 0 or negative
worst = drawdown.min()               # the deepest fall
```

`cummax` writes on each day the highest value seen up to that day. It does
not look into the future, so it can be computed for each day with what was
known on that day.

## Accumulation and comparison

```python
ytd = s.groupby(s.index.year).cumsum()                    # each year starts from zero
share = s.groupby(s.index.year).cumsum() / s.groupby(s.index.year).transform("sum")
```

The first accumulates each year on its own; the second answers "what share
of the year is done". Putting two years side by side by day number
(`dayofyear`) shows which one is ahead.

## Properties of returns

Three observations you will meet again and again in price series:

- **The price level is very persistent; the return is not.** Today's price is
  tied 0.99 to yesterday's; today's return is hardly tied to yesterday's at
  all.
- **Volatility clusters.** Big changes are followed by big changes; calm
  stretches stay calm. The **size** of the return is more predictable than
  the return itself.
- **Extremes are more frequent than expected.** The distribution of daily
  returns has fatter tails than the bell curve.

That is why the standard approach with price series is to model the return,
not the level.
