Two versions of a dataset are given as lists of rows; every row has an `"id"`. Write the function `diff_versions(old, new)` and return a dictionary:

- `"added"`: the identifiers in `new` but not in `old`.
- `"removed"`: the identifiers in `old` but not in `new`.
- `"changed"`: the identifiers in both whose row is different.

Every list should be **sorted**. The order of the rows in the list doesn't matter: match the rows by identifier.

**Expected output:**

```
added ['C4']
removed ['C1']
changed ['C2']
```
