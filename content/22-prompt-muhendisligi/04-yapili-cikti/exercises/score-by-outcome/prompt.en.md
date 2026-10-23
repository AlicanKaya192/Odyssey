`score_outcomes(pairs)` should take a list of `[expected, got]` pairs and
return a dictionary:

- For every outcome in `LABELS`, `[right, total]`: of the pairs whose
  expected outcome is that one, how many also got it.
- `"false_accept"`: the number of pairs that got `"accepted"` while
  something else was expected. This is the costliest error: an answer that
  should have been asked about or rejected was accepted.

**Expected output:**

```
accepted [1, 2]
rejected [1, 2]
needs_clarification [0, 1]
false_accept 2
```
