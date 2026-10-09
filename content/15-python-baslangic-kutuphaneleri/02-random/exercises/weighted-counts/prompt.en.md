Write the function `weighted_counts(options, weights, k, seed)`: make `k`
picks from `options` with the weights `weights` using the `choices` method of
a `random.Random(seed)` generator, and return how many times each option came
as a dictionary. An option that never came must also be in the dictionary
with `0`.

**Expected output:**

```
{'red': 716, 'green': 177, 'blue': 107}
```
