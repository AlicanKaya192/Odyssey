Formulas and code for sampling and approximation.

## Taking a sample

```python
df.sample(n=10_000, random_state=42)          # exactly 10 000 rows
df.sample(frac=0.01, random_state=42)         # one percent
df.groupby("city", group_keys=False).sample(n=200, random_state=0)  # stratified
```

## Standard error and confidence interval

```text
standard error (SE) = s / √n            (s: the sample's standard deviation)
95% confidence interval = estimate ± 1.96 × SE
```

```python
se = s["unit_price"].std() / np.sqrt(len(s))
low, high = s["unit_price"].mean() - 1.96 * se, s["unit_price"].mean() + 1.96 * se
```

## How many rows are needed?

To estimate the mean with a margin of error ± E (with 95% confidence):

```text
n ≈ (1.96 × σ / E)²
```

σ is the data's standard deviation (if you do not know it, estimate it from a
small pilot sample). For the order prices σ = 841.6:

| Margin of error wanted (E) | Sample needed |
|---|---|
| ± 50 lira | 1 089 |
| ± 20 lira | 6 803 |
| ± 10 lira | 27 209 |
| ± 5 lira | 108 834 |

Halving the error takes four times the data.

## This track's measurements

| Sample | Spread of the estimates (lira) |
|---|---|
| 100 | 87.6 |
| 1 000 | 25.8 |
| 10 000 | 8.2 |
| 100 000 | 2.4 |

191 of 200 confidence intervals (95.5%) contained the real mean.

## Sampling while reading

```python
rng = random.Random(42)
pd.read_csv("orders.csv", skiprows=lambda i: i > 0 and rng.random() > 0.01)
```

## Reservoir sampling

```python
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
```

## DuckDB

```sql
... USING SAMPLE 1% (bernoulli, 42)     -- one percent, seed 42
... USING SAMPLE 10000 ROWS             -- exactly 10 000 rows
approx_count_distinct(x)                -- approximate number of distinct values
approx_quantile(x, 0.5)                 -- approximate median
```
