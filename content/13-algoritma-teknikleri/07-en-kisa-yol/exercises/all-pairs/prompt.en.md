Write the function `all_pairs(n, edges)` **with Floyd–Warshall**: the nodes
are `0`..`n − 1`, the edges `[a, b, weight]` are **undirected**. It returns
the `n × n` distance table; `-1` for an unreachable pair.

At the start `d[i][i] = 0`, edges get their weight, the rest infinity. Then
for every `k`, every `i, j`: update if `d[i][k] + d[k][j] < d[i][j]`.

**Expected output:**

```
[0, 3, 4, -1]
[3, 0, 1, -1]
[4, 1, 0, -1]
[-1, -1, -1, 0]
```
