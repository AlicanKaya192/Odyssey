Write the function `sort_by_score(records)` with merge sort: it sorts
`[name, score]` pairs **by score ascending**; those with equal scores must
**keep their input order** (stable).

- `[["Bora", 2], ["Ada", 2], ["Cem", 1]]` →
  `[["Cem", 1], ["Bora", 2], ["Ada", 2]]` (Bora was before Ada in the input)

Compare scores while merging (`left[i][1] <= right[j][1]`); `<=` provides the
stability. Do not use `sorted` or `.sort()`.

**Expected output:**

```
[['Cem', 1], ['Bora', 2], ['Ada', 2]]
[['y', 3], ['w', 3], ['x', 5], ['z', 5]]
```
