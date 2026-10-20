Write the function `changed_weights(names, old, new, limit)` that compares two models' weights:

- For every feature compute the difference `new - old`, round it to two digits.
- If the difference's absolute value is greater than `limit`, add `[name, difference]`.
- Sort the result by the difference's absolute value from largest to smallest (keep the original order for ties).

**Expected output:**

```
['fee', 1.02]
['calls', -0.78]
[]
```
