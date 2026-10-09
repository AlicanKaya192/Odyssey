Write the function `bootstrap_ci(values, reps, seed)`: it returns the 95%
bootstrap interval of the mean as a tuple `(low, high)`. The generator is
`rng = random.Random(seed)`.

`reps` times: take a sample with replacement with
`rng.choices(values, k=len(values))` and add its mean (`sum / len`) to a list.
Sort the list; `low = means[int(0.025 * reps)]`,
`high = means[int(0.975 * reps)]`, both `round(..., 2)`.

**Expected output:**

```
(74.3, 85.8)
(5.0, 5.0)
```
