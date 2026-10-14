`histogram_sample(name, bins, n, seed)` should produce `n` samples from the
histogram of the species' weights (`np.histogram(weights, bins=bins)`): the
generator is `g = np.random.default_rng(seed)`; the bin with
`g.choice(len(p), size=n, p=p)`, the value with
`g.uniform(edges[box], edges[box + 1])`. Return `[mean, standard deviation]`
as `float`s rounded to 1 place.

**Expected output:**

```
[552.1, 106.6]
[306.8, 71.1]
```
