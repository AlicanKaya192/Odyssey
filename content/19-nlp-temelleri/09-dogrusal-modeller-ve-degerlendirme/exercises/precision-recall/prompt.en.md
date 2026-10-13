`prf(y_true, y_pred, label)` should return `[precision, recall, F1]` (3
places) for the given class. If a denominator is 0, that measure is `0.0`:

- precision = correct predictions / all predicted as that class
- recall = correct predictions / all truly of that class
- F1 = 2PR / (P + R)

**Expected output:**

```
[0.5, 0.333, 0.4]
[0.6, 0.75, 0.667]
```
