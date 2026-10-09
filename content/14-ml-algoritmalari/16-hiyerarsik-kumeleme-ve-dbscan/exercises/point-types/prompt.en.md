Write the function `point_types(X, eps, min_samples)`: for every point
`"core"`, `"border"` or `"noise"`. Core: at least `min_samples` points
(itself included) within `eps`. Border: not core but has a core point within
`eps`. The rest is noise. Return the list.

**Expected output:**

```
0 core
1 core
2 core
3 core
4 border
5 noise
```
