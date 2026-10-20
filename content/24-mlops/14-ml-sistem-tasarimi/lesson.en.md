# ML System Design

In this module we built the parts one by one: reproducible training,
validation, the registry, serving, monitoring, retraining, the canary,
scaling. **ML system design** is deciding, before writing code, which of
these parts come together and how. Design starts with a series of
questions; in this section we list them and answer the two most important
by measuring: what is success measured by, and what happens if the model
goes down?

## Design questions

| Question | The answer in this example |
|---|---|
| What is the business goal? | Reduce churn: offer a discount to customers at risk |
| What is the ML task? | Binary classification; the churn probability |
| What is success measured by? | A **business measure** (profit); accuracy is a helper measure |
| When do labels arrive? | A month later; this is a **label delay** |
| When is the prediction made? | In batch, every night (Scaling) |
| What is the baseline? | A simple rule or making no offers |
| What if the model goes down? | A **fallback** |
| What is monitored? | Drift, calibration and the business measure (Monitoring) |

The order of the questions matters: choosing the model isn't even in the
middle of the list. The goal and the measure are written first, because
without them there is no such thing as a "good model".

The shared pieces: the model, the test customers, the probabilities and
the labels.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from ml_data import make_customers, NUMERIC


def features(r):
    return [r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


train = make_customers(2000)
model = make_pipeline(StandardScaler(), LogisticRegression())
model.fit([features(r) for r in train], [r["churned"] for r in train])
test = make_customers(1000, seed=99)
probs = model.predict_proba([features(r) for r in test])[:, 1]
labels = [r["churned"] for r in test]
print(sum(labels), "of", len(test), "customers churned")
```

```text
297 of 1000 customers churned
```

## Writing the business measure

The model's job is to make a decision: who gets an offer? Writing down the
decision's value needs a few assumptions. Suppose that:

- An offer costs **5 units**.
- A customer who would churn accepts the offer with a **30%** probability
  and stays, and a customer who stays is worth **60 units**. So the
  expected return of an offer to someone who would churn is 0.3 × 60 =
  **18 units**.
- An offer to a customer who would stay anyway is wasted: it only costs.

These numbers are an example; in a real business they come from the
marketing and finance teams. But they must be written down: they decide
the threshold.

```python
COST, SAVED = 5, 18


def profit(threshold):
    offered = [y for p, y in zip(probs, labels) if p >= threshold]
    return len(offered), sum(SAVED * y - COST for y in offered)


def accuracy(threshold):
    hits = sum((p >= threshold) == bool(y) for p, y in zip(probs, labels))
    return round(hits / len(labels), 3)


for threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    offers, total = profit(threshold)
    score = accuracy(threshold)
    print(f"{threshold}: {offers:>3} offers, profit {total:>5}, accuracy {score}")
```

```text
0.1: 651 offers, profit  1803, accuracy 0.614
0.2: 474 offers, profit  2166, accuracy 0.733
0.3: 363 offers, profit  2235, accuracy 0.79
0.4: 272 offers, profit  2150, accuracy 0.821
0.5: 204 offers, profit  1806, accuracy 0.813
0.6: 152 offers, profit  1580, accuracy 0.811
0.7: 100 offers, profit  1192, accuracy 0.791
```

The threshold where accuracy is best and the threshold where profit is
best are **not the same**. Accuracy counts a wasted offer and a missed
customer equally; but here a missed customer (18 units) is much more
expensive than a wasted offer (5 units). That's why profit grows at a
lower threshold that makes more offers.

## The best threshold

Let's try the thresholds one by one and pick the one with the largest
profit:

```python
candidates = [t / 100 for t in range(5, 96)]
best = max(candidates, key=lambda t: profit(t)[1])
print("best threshold:", best, profit(best), "accuracy", accuracy(best))
print("default 0.5:", profit(0.5), "accuracy", accuracy(0.5))
print("offer everyone:", profit(0.0))
```

```text
best threshold: 0.31 (352, 2254) accuracy 0.797
default 0.5: (204, 1806) accuracy 0.813
offer everyone: (1000, 346)
```

The threshold with the largest profit is 0.31: 448 units
more profit than the default 0.5, with slightly lower accuracy. Offering
everyone isn't an option either: the cost almost eats the return. The
model is the same model; only the **measure** changed. As in the Model
Registry section, the threshold is written into the registry with the
model and chosen again when the business assumptions change.

The threshold was chosen on this test set; to be honest, it must be
confirmed on another period (the winner's curse from Experiment
Tracking).

## The fallback

What happens if the model server goes down, the latency limit is
exceeded, or the registry gives a broken model? In a good design the
answer is written in advance: a **fallback**. The simplest is a rule known
even before the model: "make an offer to whoever called the support line
at least twice."

```python
rule = [y for r, y in zip(test, labels) if r["support_calls"] >= 2]
print("model:", profit(best))
print("rule: ", (len(rule), sum(SAVED * y - COST for y in rule)))
print("nothing:", (0, 0))
```

```text
model: (352, 2254)
rule:  (172, 1066)
nothing: (0, 0)
```

The rule brings about half of the model's profit. When the model goes
down, the rule runs instead of no offers going out at all; not all of the
profit is lost, only about half. The rule is also the **baseline**: if
the model isn't better than the rule, it isn't worth its complexity.

The fallback must be tested too: a fallback that has never run may not
run when it is needed. Really running it now and then on a small share of
the traffic, as in a canary, shows that it works.

## Writing the design down

The design is written into a document; the code comes after. The sections
of a short design document:

| Section | What it contains |
|---|---|
| Goal | The business goal and the business measure, with assumptions |
| Data | Sources, labels and the label delay, validation |
| Model | Baseline, candidate models, the threshold and how it was chosen |
| Serving | Batch or online, latency limit, fallback |
| Monitoring | Drift, calibration, the business measure; alerts |
| Retraining | Schedule or trigger, the gate set |

Every section of this module fills one row of this table.

## Summary

- ML system design starts with questions asked before writing code;
  choosing the model isn't at the top of the list.
- Success is written with a **business measure**; its assumptions are
  written explicitly.
- The lesson's measurement: the threshold best for accuracy and the one
  best for profit differ (0.31, 448 units more than the
  default 0.5).
- The threshold is written into the registry with the model and confirmed
  on another period.
- A **fallback** is written in advance and tested; a simple rule is both
  the fallback and the baseline.
- The design document: goal, data, model, serving, monitoring,
  retraining.
