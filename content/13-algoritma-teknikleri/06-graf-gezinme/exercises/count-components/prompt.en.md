Write the function `count_components(n, edges)`: it returns how many
**connected components** the nodes numbered `0` to `n − 1` split into. A node
with no edges is a component on its own.

Start a new BFS (or DFS with a stack) from every node not yet visited. On the
200,000-node chain on the last line, recursive DFS hits the depth limit.

**Expected output:**

```
2
4
1
```
