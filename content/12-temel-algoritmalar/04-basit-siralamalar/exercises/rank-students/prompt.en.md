In this exercise you use Python's `sorted` function with `key=`.

Write the function `rank(records)`: `records` is a list of `[name, score]`
pairs. It sorts the students **by score from highest to lowest**, those with
equal scores **alphabetically by name**, and returns only the names.

- `[["Cem", 80], ["Ada", 92], ["Bora", 80]]` → `["Ada", "Bora", "Cem"]`

**The idea:** use a tuple key; taking the **negative** of the score sorts from
highest to lowest.

**Expected output:**

```
['Ada', 'Bora', 'Cem']
['Lale', 'Mert', 'Zeki']
```
