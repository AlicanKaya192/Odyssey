# Sampling and Approximation

So far we have asked every question of **all** the data. Often there is no
need. To find out whether a pot of soup is salty enough you do not drink the
whole pot; you stir it well and taste a spoonful. Data works the same way: a
well-chosen **sample** gives an answer very close to the truth with much less
work than all the data. What is more, you can also say how far that answer
might be off.

In this section we see how a sample is taken, how reliable it is, which
samples mislead, and big data tools' "not exact but very close and very
cheap" calculations.

The examples have a million orders. The real mean price (from all the data):

```python
import numpy as np
import pandas as pd
from orders_data import make_orders

orders = make_orders(1_000_000)
print(round(orders["unit_price"].mean(), 2))
```

```text
736.87
```

## A random sample

`sample` picks random rows from a table. `random_state` is the seed of the
randomness: the same number gives the same rows every time, so the result can
be repeated.

```python
s = orders.sample(n=10_000, random_state=42)
est = s["unit_price"].mean()
print(round(est, 2))
```

```text
729.31
```

With one percent of a million rows we found 729.31 instead of 736.87. But how
good is that? Another sample would give another number; a single estimate does
not answer "how far off might I be?".

## How far off might I be? The standard error

Statistics has an answer to this question: the **standard error**. It
estimates how much the sample mean moves around from one random sample to the
next:

```text
standard error = the sample's standard deviation / √(sample size)
```

The real value lies within about **1.96 standard errors** either side of the
estimate; this range is called the **95% confidence interval**:

```python
se = s["unit_price"].std() / np.sqrt(len(s))
low, high = est - 1.96 * se, est + 1.96 * se
print(round(se, 2), round(low, 2), round(high, 2))
```

```text
8.33 712.99 745.64
```

The estimate is 729.31 and the interval runs from 712.99 to 745.64; the real
value 736.87 is inside the interval. You saw confidence intervals with their
formulas in the Mathematics track; here we use them as a big data tool.

### What does "95%" mean?

I repeated the same work with 200 different random samples and checked each
time whether the interval contained the real value:

```python
true_mean = orders["unit_price"].mean()
hits = 0
for i in range(200):
    s = orders["unit_price"].sample(n=10_000, random_state=i)
    se = s.std() / np.sqrt(len(s))
    if s.mean() - 1.96 * se <= true_mean <= s.mean() + 1.96 * se:
        hits += 1
print(hits)
```

```text
191
```

In 191 of the 200 tries (95.5 percent) the interval caught the real value.
That is exactly what "95% confidence" means: about 95 percent of the intervals
built this way contain the real value.

## How does the error shrink as the sample grows?

I took 200 samples of each of several sizes and measured how much the
estimates were spread out (their standard deviation):

```python
for n in [100, 1_000, 10_000, 100_000]:
    means = [orders["unit_price"].sample(n=n, random_state=i).mean() for i in range(200)]
    print(n, round(np.std(means), 2))
```

```text
100 87.6
1000 25.82
10000 8.2
100000 2.39
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>100 rows</span><span>estimates move ± 87.6 lira</span></div>
    <div class="anat-row"><span>1 000 rows</span><span>± 25.8 lira</span></div>
    <div class="anat-row"><span>10 000 rows</span><span>± 8.2 lira</span></div>
    <div class="anat-row"><span>100 000 rows</span><span>± 2.4 lira</span></div>
  </div>
  <figcaption>On each row the sample grows tenfold and the error falls to about a third: the error shrinks with 1/√n.</figcaption>
</figure>

When the sample grows **tenfold**, the error falls to about **a third**
(√10 ≈ 3.16). To halve the error you need four times the data; to cut it to a
tenth, a hundred times. This is the **square root rule**.

It has an important consequence for big data: the error depends on the size
of the **sample**, not of all the data. A random sample of 10 000 rows taken
from a million rows or from a billion estimates the mean with similar
accuracy. The bigger the data, the more a sample is worth.

## A bad sample: the first N rows

The easiest sample looks like `head`: "let me look at the first 10 000 rows".
Let us compare two samples:

```python
for name, part in [("head", orders.head(10_000)),
                   ("random", orders.sample(n=10_000, random_state=1))]:
    t = pd.to_datetime(part["order_time"])
    print(name, t.dt.month.nunique(), t.min().date(), t.max().date())
```

```text
head 1 2024-01-01 2024-01-04
random 12 2024-01-01 2024-12-31
```

Since the orders were written in time order, the first 10 000 rows are only
the **first four days** of the year. Everything that is not early January
(holidays, summer, the year-end campaign) is missing from this sample. The
random sample, on the other hand, comes from all twelve months.

This is **bias**: the sample does not represent the whole. The most dangerous
thing about bias is that a bigger sample does not fix it. The first million
rows are still just the "first" rows.

## Stratified sampling

A random sample carries the proportions of the whole: Istanbul is 34 percent
of the orders, Trabzon 5 percent. In a sample of 1 600 rows that means 536
orders for Istanbul and 75 for Trabzon. If you want to **compare** cities,
Trabzon's estimate is made with little data and moves around a lot.

**Stratified sampling** splits the data into groups (strata) and takes a
separate sample from each. Equal numbers from every city, 200 each:

```python
strat = orders.groupby("city", group_keys=False).sample(n=200, random_state=0)
```

I repeated both ways 200 times with the same total size (1 600) and measured
the mean error of each city's mean price estimate:

| City | Simple random | 200 from each city |
|---|---|---|
| Istanbul | 25.9 | 47.4 |
| Ankara | 42.2 | 47.6 |
| Izmir | 45.6 | 48.1 |
| Trabzon | 74.2 | 47.2 |

With the stratified sample every city's error is similar; Trabzon's error
fell from 74.2 to 47.2. The price is paid in Istanbul: with 200 orders
instead of 536 its error grew. If you will compare groups, stratified; if you
need a single number for the whole, simple random.

## Sampling while reading

Reading a whole file and then taking a sample means taking all the data into
memory. `read_csv`'s `skiprows` option can take a function; it asks "skip
it?" for each row:

```python
import random

rng = random.Random(42)
part = pd.read_csv("orders.csv", skiprows=lambda i: i > 0 and rng.random() > 0.01)
print(len(part))
```

```text
9962
```

- `i > 0`: row 0 holds the column names; never skip it.
- `rng.random() > 0.01`: skip each row with a 99 percent chance, that is,
  keep about one percent.

Memory holds only the chosen rows (0.96 MB). On this computer reading took
0.47 seconds, reading the whole file 1.37 seconds: the skipped rows are still
scanned from start to end, but not turned into a table.

## A stream of unknown length: reservoir sampling

Sometimes you do not know how many rows are coming: the data arrives from a
stream, or the file is so big that even counting is a job. Is it possible to
pass through the stream once and take a sample of **exactly k** items that
gives every item an equal chance? Yes: **reservoir sampling**.

```python
import random

def reservoir(items, k, seed):
    rng = random.Random(seed)
    sample = []
    for i, item in enumerate(items):
        if i < k:
            sample.append(item)
        else:
            j = rng.randint(0, i)
            if j < k:
                sample[j] = item
    return sample

print(sorted(reservoir(range(1, 1_000_001), 10, seed=7)))
```

```text
[241872, 242003, 265420, 441598, 474876, 500179, 562811, 653273, 783341, 819875]
```

The idea:

1. Put the first k items into the reservoir.
2. For every later item (the i-th), draw a random number between 0 and i. If
   the number is smaller than k, that item takes the place of an item in the
   reservoir.
3. When the stream ends, the k items in the reservoir have been chosen with
   equal chance from all the items that came.

Memory holds only k items at any moment, however long the stream. I measured
the "equal chance" claim: over 2 000 samples of 10 items from 0–999, 10 022
of those chosen came from the lower half and 9 978 from the upper half.

## Sampling in DuckDB

DuckDB can take the sample inside the query:

```sql
SELECT avg(unit_price) FROM 'orders.parquet' USING SAMPLE 1% (bernoulli, 42);
SELECT * FROM 'orders.parquet' USING SAMPLE 10000 ROWS;
```

- `1% (bernoulli, 42)`: take each row with a one percent chance, seed 42. Run
  twice, both gave 9 881 rows: the seed fixes the result.
- `10000 ROWS`: exactly 10 000 rows.

## Approximate calculations

Some questions are expensive to answer exactly. To answer "how many different
customers are there?" exactly you need to see each customer once and remember
it (the set from Section 3). With hundreds of millions of different values,
that set may not fit in memory.

**Approximate algorithms** answer these questions with a fixed, very small
memory and a small margin of error:

```python
import duckdb

duckdb.sql("SELECT count(DISTINCT customer_id) FROM 'orders.parquet'")
duckdb.sql("SELECT approx_count_distinct(customer_id) FROM 'orders.parquet'")
duckdb.sql("SELECT median(unit_price) FROM 'orders.parquet'")
duckdb.sql("SELECT approx_quantile(unit_price, 0.5) FROM 'orders.parquet'")
```

The results on this computer:

| Question | Exact | Approximate |
|---|---|---|
| Number of different customers | 245 461 (0.056 s) | 219 479 (0.018 s) |
| Median price | 449.05 (0.056 s) | 449.18 (0.080 s) |

- For the number of different values the approximate result came out 10.6
  percent short but was three times faster. Behind this kind of counting is
  an algorithm called **HyperLogLog**; however many different values there
  are, it uses a small, fixed amount of memory.
- For the median the approximate result is very close, but at this size it
  came out **slower** than the exact calculation. A million rows is still
  small for one machine; the real gain of approximate methods is in memory
  and in combining the results of many machines. Each machine produces a
  small summary and the summaries combine; an exact median, on the other
  hand, needs all the values gathered in one place.

## When a sample, when all of it?

**A sample suits:** exploring data, seeing the overall shape of a chart,
trying a method quickly, "approximate" numbers on dashboards.

**All of it is needed:** numbers that must be right to the penny, such as
invoices, accounting and salaries; **rare events** (fraud, failures): a one
percent sample easily misses events that happen once in a thousand.

## Summary

- `df.sample(n=..., random_state=...)` takes a random sample; the seed makes
  the result repeatable.
- Standard error = standard deviation / √n; the 95% confidence interval is the
  estimate ± 1.96 standard errors. In this measurement 191 of 200 intervals
  contained the real value.
- The error depends on the size of the sample, not of all the data; when the
  sample grows tenfold the error falls to a third.
- Regular choices such as `head` are biased: the first 10 000 orders are the
  first four days of the year.
- If you will compare groups, a stratified sample:
  `groupby(...).sample(n=...)`.
- To sample while reading, `read_csv(skiprows=function)`; for a stream of
  unknown length, reservoir sampling.
- Approximate counting and percentiles work with a small, fixed memory; they
  are not used for work that needs exact values or for rare events.
