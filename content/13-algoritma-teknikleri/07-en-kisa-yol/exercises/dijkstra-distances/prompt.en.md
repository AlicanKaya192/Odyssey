Write the function `shortest_distances(graph, start)` **with Dijkstra**:
`graph` is `{node: {neighbour: weight}}`; it returns the shortest distance to
every node reachable from `start` as a dictionary sorted by name.

Push `(distance, node)` to the heap; skip a popped node if it was settled
before; if `d + w` is shorter for a neighbour, update it and push it.

**Expected output:**

```
A [0, 3, 2, 8, 10, 13]
F [13, 10, 11, 5, 3, 0]
```
