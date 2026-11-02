`risk_score(likelihood, impact)` should return the product of the two
scores. But if one of the scores is not between 1 and 5 (both included),
the calculation makes no sense: return `None` in that case.

**Expected output:**

```
12
25
None
None
```
