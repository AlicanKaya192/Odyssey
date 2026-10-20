# A/B Tests, Shadow and Canary

In the Concept Drift section the new model passed the gate on a current
set. But the gate is an **offline** test: it measures on recorded data.
Other things happen live: real requests, real latency, a configuration
error on the server. Instead of opening the new model to every customer at
once, there are three ways to release it step by step while measuring:
**shadow**, **canary** and the **A/B test**.

| | Shadow | Canary | A/B test |
|---|---|---|---|
| Does the customer see the new model's answer | No | A small share does | Half the group does |
| Risk | None | Small, limited | Some, but measured |
| What it answers | Does the new model work live, how different is it? | Is it broken? | Is it really better? |

The shared pieces: the old model, the new model trained on the last
window, and today's customers (month 6).

```python
import zlib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC


def features(r):
    return [r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


def fit(rows):
    model = make_pipeline(StandardScaler(), LogisticRegression())
    return model.fit([features(r) for r in rows], [r["churned"] for r in rows])


def accuracy(model, rows):
    return model.score([features(r) for r in rows], [r["churned"] for r in rows])


old = fit(make_customers(2000))
window = make_customers(500, seed=7, month=4) + make_customers(500, seed=7, month=5)
new = fit(window)
today = make_customers(1000, seed=99, month=6)
X = [features(r) for r in today]
print(len(today), "customers today")
```

```text
1000 customers today
```

## Shadow

In shadow mode the new model runs next to the old one: it gets every
request too and gives its answer, and the answer is **recorded but not
used**. The customer sees only the old model's answer:

```python
served = old.predict(X)
shadow = new.predict(X)
print("different answers:", int((served != shadow).sum()))
print("churn share:", served.mean(), "vs", shadow.mean())
scores = [round(accuracy(model, today), 3) for model in (old, new)]
print("later, with labels:", scores)
```

```text
different answers: 298
churn share: 0.586 vs 0.456
later, with labels: [0.685, 0.821]
```

The first two lines are visible **without waiting** for labels: the two
models decide differently for 298 customers, and the new model
expects much less churn. A difference this large is neither good nor bad;
it only says "look carefully". When the labels arrive, the third line
decides: the new model is better by far.

The price of shadow mode is twice the computation; its risk is zero. It
also shows that the new model **works** in the live environment (doesn't
error, answers in time), which an offline test can't show.

## Canary

In a canary a small share of the traffic goes to the new model; if there
is no problem the share grows step by step: 1%, 5%, 25%, 50%, 100%. The
name comes from the canary miners took into the mine: it notices the
danger first.

Who goes to the new model? Rolling a die on every request
(`random.random()`) sends the same customer once to the old and once to
the new model; the customer sees inconsistent answers. Instead, a
**bucket** is computed from the customer's id:

```python
def route(customer_id, percent):
    bucket = zlib.crc32(str(customer_id).encode()) % 100
    return "new" if bucket < percent else "old"


for percent in [1, 5, 25, 50]:
    count = sum(route(r["id"], percent) == "new" for r in today)
    print(f"{percent:>3}% -> {count} customers")
```

```text
  1% -> 8 customers
  5% -> 39 customers
 25% -> 238 customers
 50% -> 491 customers
```

`zlib.crc32` always gives the same number for the same id (the same idea
as partitioning in the Big Data path); the customer always stays on the
same model. There is one more plus: a bucket below 5 is also below 25, so
a customer who saw the new model at 5% keeps seeing it at 25%. The counts
don't match the percentages exactly; the buckets don't spread perfectly
evenly over 1000 customers.

## A broken model in the canary

Suppose the new model's server has the bug from the Training-Serving Skew
section: the columns go in reverse order. At every canary stage let's
measure the healthy new model and the broken one on the same customers:

```python
def healthy(rows):
    return new.predict([features(r) for r in rows])


def broken(rows):
    return new.predict([features(r)[::-1] for r in rows])


def canary_score(predict, rows, percent):
    canary = [r for r in rows if route(r["id"], percent) == "new"]
    hits = sum(p == r["churned"] for p, r in zip(predict(canary), canary))
    return len(canary), round(hits / len(canary), 3)


for percent in [1, 5, 25]:
    n, good = canary_score(healthy, today, percent)
    bad = canary_score(broken, today, percent)[1]
    print(f"{percent:>3}% n={n:<4} healthy {good:.3f} broken {bad:.3f}")
```

```text
  1% n=8    healthy 0.875 broken 0.500
  5% n=39   healthy 0.795 broken 0.538
 25% n=238  healthy 0.832 broken 0.529
```

The broken model looks bad at every stage, even at 1%. But at 1% the
canary has only 8 customers. Let's repeat the same 1% for ten
days, with new customers every day:

```python
for day in range(1, 11):
    rows = make_customers(1000, seed=99 + day, month=6)
    good = canary_score(healthy, rows, 1)[1]
    bad = canary_score(broken, rows, 1)[1]
    print(f"day {day:>2}: healthy {good:.3f} broken {bad:.3f}")
```

```text
day  1: healthy 0.750 broken 0.375
day  2: healthy 0.750 broken 0.125
day  3: healthy 0.875 broken 0.000
day  4: healthy 0.750 broken 0.500
day  5: healthy 0.750 broken 0.250
day  6: healthy 0.500 broken 0.375
day  7: healthy 0.750 broken 0.750
day  8: healthy 1.000 broken 0.750
day  9: healthy 1.000 broken 0.250
day 10: healthy 0.625 broken 0.375
```

With eight customers the broken model's score swings between
0.000 and 0.750; on day 7 it gets the **same** score
as the healthy model, and someone looking that day would move it to the
next stage. The other direction happens too: on day 6 the healthy model
gets 0.500, below the old model; someone looking that day would
pull a good model back. That's why today's 1% result can't be trusted
either. At 5% with 39 customers and at 25% with 238 the
difference is clearly visible.

Two rules follow: before deciding at any stage, write down in advance **the
minimum number of customers** needed; a stage is passed only once that
many have been seen. And a canary doesn't look only at accuracy: labels
arrive late, so the error rate, latency and the prediction distribution
(the Monitoring section) are watched without labels too. If the breakage
is caught at 5%, 39 customers are affected; had the model been
released directly, it would have been all 1000.

## A/B test

In an A/B test the customers are split randomly into two groups: A sees
the old model, B the new one, and a measure is compared. The real question
is: is the difference **real or luck**?

The honest way to measure this is an **A/A test**: put the **same** model
in both groups and look at the difference. Since the model is the same,
every difference is luck. Let's repeat it 200 times while changing the
group size:

```python
for n in [100, 400, 1600]:
    gaps = []
    for s in range(200):
        a = make_customers(n, seed=1000 + s, month=6)
        b = make_customers(n, seed=5000 + s, month=6)
        gaps.append(abs(accuracy(old, a) - accuracy(old, b)))
    gaps.sort()
    print(f"n={n:<5} 95% of gaps below {gaps[int(0.95 * len(gaps))]:.3f}")
```

```text
n=100   95% of gaps below 0.130
n=400   95% of gaps below 0.062
n=1600  95% of gaps below 0.034
```

The same model, purely by luck, can show a difference of up to
0.13 with 100 customers per group. When the group grows **four
times**, the noise drops to about **half**. The difference between our two
models (0.685 → 0.821) is far above this noise. But if the noise keeps
dropping at this rate, it reaches 0.01 only at more than ten thousand
customers per group: seeing a small improvement needs a long test. First
the noise is measured, then how long the test runs is decided: stopping
the moment you see a difference is stopping when luck is at its largest.

In real A/B tests the measure compared is usually not accuracy but a
**business measure** (churn rate, revenue): if the model offers a discount
to customers it thinks will churn, the model's decision changes the
outcome too. Only an experiment run live can measure that.

## Which one when?

| Method | When | Watch out |
|---|---|---|
| Shadow | For every new model, first | Twice the computation; can't measure decisions that change the outcome |
| Canary | After shadow, the release itself | Minimum customers per stage; measures without labels |
| A/B test | For the question "is it really better?" | Noise first with A/A; the duration decided in advance |

Most teams use the three in order: they see it works in shadow, see it
isn't broken in the canary, and measure that it is really better in the
A/B test.

## Summary

- The gate is offline; releasing is measured separately.
- **Shadow:** the new model sees every request, its answer isn't used. No
  risk; the difference is visible without labels.
- **Canary:** a small share of the traffic goes to the new model, the share
  grows step by step. A bucket from the customer id (`crc32 % 100`): the
  same customer always stays on the same model.
- The lesson's measurement: at 1% there are 8 customers; the broken model's
  score swung between 0.000 and 0.750 from day to day. The minimum number
  of customers per stage is written down in advance.
- **A/B test:** is the difference real? First the noise is measured with an
  **A/A test**; when the group grows four times, the noise drops to half.
- Real A/B tests usually compare a business measure.
