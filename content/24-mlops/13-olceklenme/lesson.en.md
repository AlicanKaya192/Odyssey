# Scaling

In the Serving a Model section we set up a single server. When the number
of customers grows, the questions change: how many requests can one server
keep up with, what happens as it gets close to full, do we need to compute
the same question again and again, is a bigger model worth it? **Scaling**
is keeping the service fast and cheap while the load grows. In this
section we answer four questions by measuring.

## Batch or online?

The first question is **when** the prediction is computed:

| | Batch prediction | Online prediction |
|---|---|---|
| When | In advance, for example every night for all customers | The moment a request arrives |
| Where the result is | In a table; the application reads it from there | In the server's response |
| Plus | Cheap, simple, no speed problem | Computes with fresh information |
| Minus | The information may be a day old | The server must be up and fast |

In the Serving a Model section we measured that a batch call is at least
ten times faster per customer. For a score that changes once a day, like
churn risk, batch prediction is often enough; online prediction is needed
where the answer depends on the information of that moment (the item in
the cart, the last click).

## Utilization and waiting

With online prediction, requests arrive at random moments. A server's
**utilization** is how much of its time it is busy: if 50 requests arrive
per second and each takes 10 ms, the server is busy half of the time
(50%). What happens as the utilization grows? Let's measure with a small
simulation: requests arrive at random, each takes 10 ms on average, the
server starts at once if it is free, and if it is busy the request waits
in the queue.

```python
import heapq
import random


def simulate(load, workers, n=20000, seed=1):
    rng = random.Random(seed)
    service = 10.0
    gap = service / (load * workers)
    free = [0.0] * workers
    now, waits = 0.0, []
    for _ in range(n):
        now += rng.expovariate(1 / gap)
        start = max(now, free[0])
        waits.append(start - now)
        heapq.heapreplace(free, start + rng.expovariate(1 / service))
    waits.sort()
    return round(sum(waits) / n, 1), round(waits[int(0.95 * n)], 1)


for load in [0.5, 0.8, 0.9, 0.95, 0.99]:
    mean, p95 = simulate(load, 1)
    print(f"load {load:.2f}: mean wait {mean:>6} ms  p95 {p95:>7} ms")
```

```text
load 0.50: mean wait    9.8 ms  p95    45.3 ms
load 0.80: mean wait   36.4 ms  p95   120.9 ms
load 0.90: mean wait   74.1 ms  p95   226.6 ms
load 0.95: mean wait  147.3 ms  p95   422.8 ms
load 0.99: mean wait  329.5 ms  p95  1131.2 ms
```

`rng.expovariate` produces random gaps with a known mean: requests don't
arrive evenly, they arrive in clusters. `free` is a heap (Algorithms path)
holding when each worker becomes free: the earliest one is always first.
`heapreplace` takes it out and puts the new one in.

The result isn't linear. When the utilization goes from 50% to 90%, the
mean wait goes from 9.8 ms to 74.1 ms; at 99% it is
329.5 ms. Every request still takes only 10 ms; the rest of the time
is spent **in the queue**. A server that looks like "it still has 10%
free" is in fact slow. That's why servers are planned not for 100% but
for, say, 70% utilization.

Spreading the same utilization over more workers also makes a difference:

```python
for workers in [1, 2, 4]:
    mean, p95 = simulate(0.9, workers)
    print(f"workers={workers} at 90%: mean wait {mean:>5} ms  p95 {p95:>6} ms")
```

```text
workers=1 at 90%: mean wait  74.1 ms  p95  226.6 ms
workers=2 at 90%: mean wait  34.5 ms  p95  110.6 ms
workers=4 at 90%: mean wait  15.4 ms  p95   52.8 ms
```

The four workers are 90% busy too; but since they share one queue, when
one becomes free a waiting request goes to it at once. The wait drops from
74.1 ms to 15.4 ms. This is a plus of **horizontal scaling**
(several copies of the same server). It needs the server to be
**stateless**: every request gets the same answer whichever copy it goes
to. The server in the Serving a Model section is like that; the model is
loaded at startup, and nothing is kept between requests.

## The cache

Many requests can arrive for the same customer in a day. If the score
hasn't changed, keeping the last answer instead of computing it again
every time is the idea of a **cache**. Requests aren't spread evenly over
customers: a few customers get many, most get few. Let's imitate this
with a weighted choice and measure how much a cache of a given size
covers:

```python
from collections import OrderedDict

rng = random.Random(3)
customers = list(range(10000))
weights = [1 / (rank + 1) for rank in customers]
requests = rng.choices(customers, weights=weights, k=50000)
print(len(set(requests)), "different customers in", len(requests), "requests")


def hit_rate(size):
    cache, hits = OrderedDict(), 0
    for customer in requests:
        if customer in cache:
            hits += 1
            cache.move_to_end(customer)
        else:
            cache[customer] = True
            if len(cache) > size:
                cache.popitem(last=False)
    return round(hits / len(requests), 3)


for size in [10, 100, 1000, 5000]:
    print(f"cache {size:>4}: {hit_rate(size)} of requests answered from cache")
```

```text
6794 different customers in 50000 requests
cache   10: 0.128 of requests answered from cache
cache  100: 0.388 of requests answered from cache
cache 1000: 0.667 of requests answered from cache
cache 5000: 0.852 of requests answered from cache
```

This cache is of the **LRU** (least recently used) kind: when full, it
removes the one asked about least recently. `OrderedDict` keeps the
order, `move_to_end` moves the one just asked to the end, and
`popitem(last=False)` drops the first. Python's ready-made version of the
same idea is `functools.lru_cache`.

Room for only 100 customers covers 0.388 of the requests:
a small number of frequently asked customers carries most of the load. But
a cache has a price: **staleness**. A stored score goes stale when the
customer's information changes or when the model changes. That's why every
entry in the cache has a lifetime (TTL, time to live), and the key is not
just the customer but **customer + model version**: when a new model is
released, the old scores fall out of use by themselves.

## How big should the model be?

A bigger model means more work on every request. In a random forest every
prediction goes through all the trees. Let's grow the number of trees:

```python
from sklearn.ensemble import RandomForestClassifier
from ml_data import make_customers, NUMERIC


def features(r):
    return [r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0]


train, test = make_customers(2000), make_customers(1000, seed=99)
X, y = [features(r) for r in train], [r["churned"] for r in train]
X_test, y_test = [features(r) for r in test], [r["churned"] for r in test]
for trees in [5, 20, 100, 400]:
    model = RandomForestClassifier(n_estimators=trees, max_depth=6, random_state=0)
    model.fit(X, y)
    print(f"{trees:>3} trees: accuracy {model.score(X_test, y_test):.3f}")
```

```text
  5 trees: accuracy 0.810
 20 trees: accuracy 0.812
100 trees: accuracy 0.813
400 trees: accuracy 0.814
```

The number of trees grows 80 times, the accuracy grows by only
0.004. On this computer a prediction for a single customer takes
about 1 ms with 5 trees and tens of times longer (about 45 ms) with 400
trees. If every request takes tens of times longer, the same utilization
needs tens of times more servers. A model is not chosen by accuracy alone;
**latency and cost** are measured too, and a limit is set (for example
"p95 must not exceed 50 ms").

## Summary

| Question | Tool | The lesson's measurement |
|---|---|---|
| When to compute? | Batch or online | A batch call at least ten times faster per customer |
| How full should a server be? | Utilization planning | 9.8 ms wait at 50%, 329.5 ms at 99% |
| What do more servers gain? | Horizontal scaling | At 90%, 1 worker 74.1 ms, 4 workers 15.4 ms |
| Recompute the same question? | Cache (LRU) | Room for 100 customers: 0.388 of the requests |
| Is a bigger model worth it? | Latency against accuracy | 5 → 400 trees: 0.810 → 0.814 |

- As utilization approaches 100%, the wait doesn't grow linearly; it
  jumps. Servers are planned with headroom.
- For horizontal scaling, the server must be stateless.
- The cache key is customer + model version; entries have a lifetime.
- Latency and cost are measured when choosing a model too.
