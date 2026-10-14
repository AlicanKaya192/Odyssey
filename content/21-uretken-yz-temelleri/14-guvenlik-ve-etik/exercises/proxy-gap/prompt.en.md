`proxy_gap(feature, group)` should return a 0/1 feature's mean in the two
groups and the difference (B − A): `[mean A, mean B, difference]`, `float`s
rounded to 2 places. A large difference shows the feature may give the group
away.

**Expected output:**

```
[0.25, 0.75, 0.5]
```
