Write the function `min_cost(grid)`: `grid[r][c]` is the cost of entering that
cell. It returns the lowest total cost from the top-left (the start's cost
counts too) to the bottom-right moving in four directions.

Cells are nodes, costs are weights: Dijkstra. BFS is wrong (weighted), and a
DP that only goes right/down is wrong too (going back is sometimes cheaper).
The last line has a 150 × 150 terrain.

**Expected output:**

```
7
7
1488
```
