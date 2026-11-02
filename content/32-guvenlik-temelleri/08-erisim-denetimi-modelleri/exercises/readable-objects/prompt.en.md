Bell-LaPadula levels: `LEVELS = ["public", "internal", "secret",
"top-secret"]`. `objects` is a dictionary from object name to
classification.

`readable_objects(clearance, objects)` should return, in alphabetical
order, the names of the objects that someone with clearance `clearance`
**can read** (no read up: object's level ≤ person's level).

**Expected output:**

```
['menu', 'plan']
['menu', 'plan', 'salary']
[]
```
