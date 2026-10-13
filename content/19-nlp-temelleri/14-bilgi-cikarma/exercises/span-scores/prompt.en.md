`span_scores(found, gold)` should compare what the rule found (`found`) with the
right answers (`gold`) and return `[precision, recall]` (3 places).
Repeats count: if the same amount appears twice, it must be found twice. If
`found` is empty precision is `0.0`; if `gold` is empty recall is `0.0`.

**Expected output:**

```
[0.667, 0.667]
[0.0, 0.0]
```
