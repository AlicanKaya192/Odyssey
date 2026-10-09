Write the function `count_islands(grid)`: `grid` is rows of `"0"` and `"1"`.
Horizontally or vertically neighbouring `"1"`s are the same island. It returns
how many islands there are.

From every unvisited `"1"` start a **BFS** and mark all cells of the island.
A recursive DFS can hit the depth limit on a big island.

**Expected output:**

```
3
0
22500
```
