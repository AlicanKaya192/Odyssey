# Network Effects and Interference

Every analysis so far rested on a silent assumption: a user's outcome
depends only on **their own** group, not on which group anyone else is in.
This assumption is called **SUTVA** (the stable unit treatment value
assumption). When users share a resource (drivers, stock, an ad budget) or
influence each other (messages, shares, a friend network), the assumption
breaks: someone in B changes the outcome of someone in A. This is called
**interference**. This section measures how wrong an ordinary A/B test is
in a market with interference.

## Shared drivers

In a ride-sharing app, B is a discount that makes riders request more
rides. Each city has a fixed number of drivers; when requests exceed the
drivers, **everyone's** requests in the city are served less often. We
made the data: 100 cities, 300 riders per city.

```python
import numpy as np
from scipy import stats
from ab_data import make_market


def lift(table, column="completed"):
    m = table.groupby("group")[column].mean()
    return round(float(m["B"] / m["A"] - 1), 3)


market = make_market()
print(lift(market, "requested"), lift(market))
```

```text
0.177 0.181
```

The test that assigns riders one by one says B raises requests by
17.7% and completed rides by 18.1%. The product team
reads it as "the discount raises rides by a fifth".

## The true effect: everyone A or everyone B

Let us build the same market in two worlds: one where everyone is A and
one where everyone is B. The true effect is the difference in completed
rides between these two worlds:

```python
all_a = make_market(share_b=0.0)
all_b = make_market(share_b=1.0)
print(round(all_b["completed"].sum() / all_a["completed"].sum() - 1, 3))
a_riders = market.loc[market["group"] == "A", "completed"].mean()
print(round(a_riders / all_a["completed"].mean() - 1, 3))
```

```text
0.012
-0.071
```

If the discount were given to everyone, rides would rise by only
1.2%: since the number of drivers does not change, the extra
requests could mostly not be served. Where did the test's 18.1%
come from? The second line gives the answer: the A riders in the test took
7.1% fewer rides than in the world where everyone is A. B riders
**took** drivers from A riders. The test measured B's gain and A's loss
together; their difference is far above the true effect.

## Cluster assignment: city by city

If the interference stays within a city, the fix is to assign at the
boundary of the interference: **all** riders of a city are either A or B.
The analysis is done at the city level too, because the assigned unit is
now the city:

```python
cities = make_market(design="city")
per_city = cities.groupby(["city", "group"])["completed"].mean().reset_index()
b = per_city.loc[per_city["group"] == "B", "completed"]
a = per_city.loc[per_city["group"] == "A", "completed"]
print(len(a), len(b), round(float(b.mean() / a.mean() - 1), 3))
print(round(float(stats.ttest_ind(b, a, equal_var=False).pvalue), 3))
```

```text
50 50 -0.021
0.709
```

The city design found -2.1%, and it is not significant. Looking
at one result can mislead again; let us compare the three methods on 100
different markets:

```python
user_l, city_l, true_l = [], [], []
for s in range(3000, 3100):
    user_l.append(lift(make_market(seed=s)))
    city_l.append(lift(make_market(seed=s, design="city")))
    a0 = make_market(seed=s, share_b=0.0)["completed"].sum()
    b1 = make_market(seed=s, share_b=1.0)["completed"].sum()
    true_l.append(b1 / a0 - 1)
for name, v in [("user", user_l), ("city", city_l), ("true", true_l)]:
    print(name, round(float(np.mean(v)), 3), round(float(np.std(v)), 3))
```

```text
user 0.197 0.015
city 0.016 0.069
true 0.011 0.003
```

The columns: the average estimate and how much the estimate moves from
market to market.

- The user design says about 19.7% **in every market**; the
  truth averages 1.1%. The bias is very large but the noise
  is small: it gives the wrong answer with great confidence.
- The city design is close to the truth on average with
  1.6%, but its estimate moves by 6.9% from
  market to market: 100 cities carry much less information than 30,000
  users.

This is the basic trade-off of interference: the **unbiased but noisy**
cluster design versus the **low-noise but biased** user design. Bias does
not go away with a larger sample; noise does.

## Where to expect interference?

- **A shared resource:** drivers, couriers, stock, hotel rooms, an ad
  budget. What B takes extra is missing from A.
- **A social network:** when someone in B shares something, their friend in
  A is affected too; this time the effect **spills over** into A and the
  test shows the effect as smaller.
- **A two-sided market:** a change for buyers changes how sellers behave.

Remedies: cluster assignment (city, region, friend cluster), switching on
and off in turns by time slot (switchback), and writing the question "can
this change alter someone else's outcome?" into the plan before the test.

## Summary

- SUTVA: a user's outcome depends only on their own group; shared resources
  and networks break it.
- With a shared resource, a user-level test enlarges the effect: B takes
  from A.
- Cluster assignment removes the bias; the analysis is done at the cluster
  level and the noise grows.
- Bias does not go away with more users.
