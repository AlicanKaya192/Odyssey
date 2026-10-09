Write the function `order_by_grade(records)`: `records` is a list of
`[name, grade]` pairs with grades between 1 and 5. It returns the students'
**names** in ascending order of grade; those with the same grade must **keep
their input order**.

- `[["Ada", 3], ["Bora", 1], ["Cem", 3], ["Deniz", 2]]` →
  `["Bora", "Deniz", "Ada", "Cem"]`

Build a bucket list per grade (`buckets[grade].append(name)`), then join the
buckets in order. Do not use `sorted` or `.sort()`.

**Expected output:**

```
['Bora', 'Deniz', 'Ada', 'Cem']
[]
```
