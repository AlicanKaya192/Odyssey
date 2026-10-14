`score_by_outcome(results)` should group `[outcome, expected]` pairs by the
**expected** outcome and return a dictionary, with keys in alphabetical
order, that gives the text `"right/total"` for every group.

**Expected output:**

```
blocked 1/1
fallback 1/1
handover 1/2
sent 2/3
```
