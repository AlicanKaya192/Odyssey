`add_scores(path, pairs)` should use `shelve` to add each `[name, score]`
pair to that name's list and, at the end, return the whole shelf as a
dictionary `{name: [scores]}` (names sorted). The starter code always leaves
the lists empty: `db[name].append(...)` is not written to the record on disk.
Take the list, add to it, **assign it back**.

**Expected output:**

```
{'ada': [90, 85], 'alan': [75]}
```
