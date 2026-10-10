`age_groups(ages)` should split ages into groups with `pd.cut`: limits
`[0, 18, 40, 65, 120]`, names `["child", "young", "middle", "senior"]`.
Return the number of people in each group as `{group: count}` **in the
groups' own order**, with an empty group showing as 0
(`value_counts(sort=False)`). **Do not write a loop.**

**Expected output:**

```
('child', 2)
('young', 2)
('middle', 0)
('senior', 1)
```
