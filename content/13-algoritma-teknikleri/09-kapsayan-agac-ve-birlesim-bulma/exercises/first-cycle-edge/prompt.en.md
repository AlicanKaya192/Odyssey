Write the function `first_cycle_edge(n, edges)`: while undirected `[a, b]`
edges are added in order, it returns the edge that **closes the first cycle**
(as it appears in the list); `None` if there is never a cycle.

If an edge's two ends are already in the same group before it is added, that
edge closes a cycle.

**Expected output:**

```
[2, 0]
None
[4, 3]
```
