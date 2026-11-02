# The Experiment Question and Choosing a Metric

The Statistical Inference module taught you to read the result of an A/B
test. This module covers **setting the test up**. Setting up starts before
the result: what are we asking, what will we measure, and what has to
happen for us to say "it worked"? If these answers are not written before
the test starts, even the most correct analysis answers the wrong question.

## Question, change, metric

An experiment question has three parts:

- **The change:** what are we changing? ("The checkout button moves to the
  top of the page.")
- **The expected effect and the reason:** why should it work? ("On mobile
  the button is not visible, so people abandon the basket.")
- **The metric and the threshold:** what do we look at, and how much is
  enough? ("If the buying rate rises by at least 0.5 points.")

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>A vague question</h4>"Is the new design better?" What does better mean, what do we look at, how big a difference is enough? After the result any metric can be picked as "better".</div>
    <div class="ok"><h4>A testable question</h4>"Does moving the button to the top raise the per-user buying rate by at least 0.5 points?" The metric, the unit and the threshold are written in advance.</div>
  </div>
  <figcaption>A testable question says, before the result arrives, which number would change the decision and how.</figcaption>
</figure>

## The data: two weeks of a shop

In this module we will mostly work with a shop's user log from before the
experiment. Each row is a user:

```python
from ab_data import make_user_log

users = make_user_log()
print(users.shape)
print(users.head(3).to_string(index=False))
```

```text
(20000, 7)
user_id platform  sessions  minutes  bought  revenue  refunded
 U00001  desktop         2      6.7       0      0.0         0
 U00002   mobile         4     25.0       0      0.0         0
 U00003  desktop         3     12.7       0      0.0         0
```

- `sessions`: number of visits, `minutes`: total time,
- `bought`: did they buy (0/1), `revenue`: how much they spent,
- `refunded`: did they refund (only buyers can refund).

## Candidate metrics

Per-user averages:

```python
for col in ["sessions", "minutes", "bought", "revenue"]:
    print(col, round(users[col].mean(), 3))
buyers = users[users["bought"] == 1]
print("refund rate", round(buyers["refunded"].mean(), 3))
```

```text
sessions 3.753
minutes 21.096
bought 0.117
revenue 11.413
refund rate 0.08
```

Metrics come in three kinds:

- **Proportion:** a yes/no question, like `bought`. 11.7% of users
  bought.
- **Mean:** a continuous value, like `revenue` or `minutes`.
- **Ratio metric:** the ratio of two totals, like "revenue per order" or
  "refund rate". Its denominator is not the number of users, so it needs a
  special calculation; we will see it in the Ratio Metrics and the Delta
  Method section.

## A good metric does two things at once

**It must be meaningful:** tied to the purpose of the business. Is more
time on the page good? If people wander because they cannot find what they
want, time goes up while things get worse. Time alone is not a good target.

**It must be sensitive:** able to pull a real change out of the noise. The
**coefficient of variation**, the standard deviation divided by the mean,
roughly shows the noise.

```python
for col in ["sessions", "minutes", "bought", "revenue"]:
    x = users[col]
    print(col, round(x.std() / x.mean(), 2))
```

```text
sessions 0.82
minutes 1.1
bought 2.74
revenue 4.32
```

Revenue has the largest coefficient of variation: most people spend
nothing, a few spend a lot. From the Effect Size section we know that the
sample needed to see the same **relative** rise grows with the square of
the deviation relative to the mean. So although revenue is the business's
most important metric, it is the most "expensive" one; we will see this in
numbers in the Sample Size section.

## Primary, secondary and guardrail metrics

- **Primary metric:** the single metric that decides, chosen in advance.
  Several "primary" metrics bring back the false alarm problem of the
  Multiple Comparisons section.
- **Secondary metrics:** help understand the reason ("buying rose because
  adding to the basket rose").
- **Guardrail metrics:** things that must not get worse. If the refund
  rate, page load time or error rate gets worse while buying rises, the
  change can still be rejected.

The refund rate in this data is 8% of buyers. Its
denominator is the buyers: do not confuse it with "refunds per user".

## A different audience means a different metric

The same metric can be very different across groups:

```python
print(users.groupby("platform")["bought"].mean().round(4))
```

```text
platform
desktop    0.1290
mobile     0.1098
Name: bought, dtype: float64
```

The buying rate is higher on desktop than on mobile. If an experiment's
traffic shifts towards one group, the average changes even if the change
does nothing. Random assignment prevents this; in the A/A Tests and Sample
Ratio Mismatch section we will see how such a shift is caught.

## The experiment plan (pre-registration)

Before the test starts a one-page plan is written:

1. The question and the reason.
2. The primary metric, its unit (per user) and the expected direction.
3. The minimum detectable effect (MDE) and the practical threshold.
4. Guardrail metrics and their limits.
5. Sample size, duration, assignment split.
6. The test to be used and α.

This plan prevents changing the metric, threshold or duration after seeing
the result.

## Summary

- An experiment question states the change, the reason, the metric and the
  threshold together.
- Metrics can be proportions, means or ratio metrics.
- A good metric is tied to the business and sensitive; revenue is important
  but noisy.
- One primary metric is chosen, plus secondary and guardrail metrics.
- The plan is written before the test starts.
