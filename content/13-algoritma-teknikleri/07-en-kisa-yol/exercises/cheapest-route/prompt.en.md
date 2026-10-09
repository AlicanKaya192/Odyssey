Write the function `cheapest_route(graph, start, goal)`: it returns the
length of the shortest path and the path itself as `[length, [nodes]]`;
`None` if there is no path.

In Dijkstra, write the `parent` of every node you update; then walk back from
the goal and reverse the list.

**Expected output:**

```
[13, ['A', 'C', 'B', 'D', 'E', 'F']]
[10, ['F', 'E', 'D', 'B']]
```
