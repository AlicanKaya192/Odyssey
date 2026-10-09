Write the function `count_islands(grid)`: `#` is land, `.` is sea. Land cells
touching in four directions form an **island**; it returns how many islands
there are.

Start a walk from every land cell not yet visited and mark all the land it
touches. On the 400 × 400 map on the last line a single island is tens of
thousands of cells; a recursive walk hits the depth limit, use a queue or a
stack.

**Expected output:**

```
3
0
38
```
