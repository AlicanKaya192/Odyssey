Write the function `min_network_cost(n, roads)` with **Kruskal**: cities
`0`..`n − 1`, `roads` are `[a, b, cost]`. It returns the total cost of the
cheapest network connecting all cities; `None` if that is impossible (fewer
than `n − 1` edges were taken).

Sort the edges by cost: `sorted(roads, key=lambda r: r[2])`.

**Expected output:**

```
11
None
```
