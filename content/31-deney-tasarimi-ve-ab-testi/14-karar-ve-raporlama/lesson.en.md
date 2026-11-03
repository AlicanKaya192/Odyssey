# Deciding and Reporting

A test never ends as simply as "p < 0.05, launch". The decision depends on
**how large** the effect is, **how large** the uncertainty is and **what a
wrong decision would cost**. This section shows how to read a confidence
interval against a threshold written in advance, what to do with an
"inconclusive" result and how to turn the decision into a report everyone
reads the same way.

## Four outcomes

As in the Analysing Your First A/B Test section there is a **practical
threshold**: B must raise buying by at least 0.3 points (a smaller rise
does not cover the cost of the change). The confidence interval can fall
in four places relative to this threshold and to zero. Let us see it with
four different tests:

```python
import numpy as np
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_experiment

THRESHOLD = 0.003


def interval(test):
    k = test.groupby("group")["bought"].sum()
    n = test.groupby("group").size()
    return confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])


def verdict(low, high, threshold=THRESHOLD):
    if high < 0:
        return "harm"
    if low >= threshold:
        return "ship"
    if high < threshold:
        return "not worth it"
    return "inconclusive"


cases = {"win": (30000, 0.15, 141), "loss": (30000, -0.15, 142),
         "small": (4000, 0.12, 143), "tiny": (1500000, 0.01, 144)}
for name, (n, lift, seed) in cases.items():
    low, high = interval(make_experiment(n=n, seed=seed, lift=lift))
    print(name, round(low * 100, 2), round(high * 100, 2), verdict(low, high))
```

```text
win 1.01 2.53 ship
loss -2.95 -1.54 harm
small -1.31 2.78 inconclusive
tiny 0.03 0.24 not worth it
```

The numbers are in points (the two ends of the 95% interval):

| Result | Interval | Decision |
|---|---|---|
| `win` | entirely above the threshold | launch |
| `loss` | entirely below zero | do not launch: harmful |
| `small` | contains both zero and the threshold | inconclusive: not enough data |
| `tiny` | above zero but entirely below the threshold | the effect is real but not worth it |

The last line matters: the `tiny` test with 1.5 million users finds a
**significant** difference, but even the top of its interval is below the
threshold. "Statistically significant" and "worth doing" are not the same;
the distinction from the Effect Size section becomes a decision here.

## What to do with an inconclusive result?

The `small` test was run with 4000 people; its interval is between
-1.31 and 2.78 points. This does not mean "B does not
work", it means "we do not know". There are three ways:

1. **More data:** extending the test with the calculation from the Sample
   Size section (if planned in advance).
2. **Reporting what the interval says:** saying "the upper bound of the
   rise is 2.78 points" is information too.
3. **Asking about the risk:** if we choose B and are wrong, what do we
   lose? With the Beta distributions from the An Introduction to the
   Bayesian View section:

```python
small = make_experiment(n=4000, seed=143, lift=0.12)
k = small.groupby("group")["bought"].sum()
n = small.groupby("group").size()
rng = np.random.default_rng(1401)
pa = rng.beta(1 + k["A"], 1 + n["A"] - k["A"], 200000)
pb = rng.beta(1 + k["B"], 1 + n["B"] - k["B"], 200000)
print(round(float((pb > pa).mean()), 3))
print(round(float(np.maximum(pa - pb, 0).mean() * 100), 3))
```

```text
0.76
0.146
```

The probability that B is better is 0.76. The second number
is the **expected loss**: the average difference we would lose in the
cases where we chose B and were wrong (0.146 points). If the
change is cheap and reversible, a small expected loss can be accepted; if
it is expensive and lasting, more data is awaited. This threshold, like
the practical threshold, is written before the test starts.

## Turning the effect into money

Decision makers often ask for money, not points. Convert the effect as an
interval, not as a single number. For 2 million visitors a year and an
average basket of 100 TL, the `win` test:

```python
visitors, basket = 2_000_000, 100
low, high = interval(make_experiment(n=30000, seed=141, lift=0.15))
print(round(low * visitors * basket), round(high * visitors * basket))
```

```text
2023143 5053874
```

The extra yearly sales are between 2,023,143 and 5,053,874 TL.
Writing a single number hides the width of the interval; as in the Novelty
Effects and Long-Term Impact section, a short test's effect can shrink over
time.

## The report

A good test report does not exceed one page and always follows the same
order:

1. **Question and decision rule:** what, with which metric, at which
   threshold (as written before the test).
2. **Trust checks:** SRM, A/A, balance.
3. **Primary metric:** the two rates, the difference, the confidence
   interval, p.
4. **Guardrail and secondary metrics:** any breakage; secondary metrics do
   not decide.
5. **Decision:** which of the four outcomes, and why.
6. **Limits:** duration, novelty effect, segments, interference risk.

## Summary

- The decision follows where the confidence interval sits relative to zero
  and to a practical threshold written in advance: launch, harmful,
  inconclusive, not worth it.
- Being significant is not the same as being worth doing.
- An inconclusive result does not mean "no effect"; it needs more data,
  reporting the interval, or weighing the expected loss.
- The money value is written as an interval.
- The report always follows the same order, short and tied to rules
  written in advance.
