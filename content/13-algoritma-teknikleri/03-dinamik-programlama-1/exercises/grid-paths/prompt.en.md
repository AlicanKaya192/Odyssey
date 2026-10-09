Write the function `grid_paths(grid)`: `grid` is a list of strings, `.` is an
empty cell, `#` a block. It returns how many paths there are from the top-left
to the bottom-right moving only **right and down**. `0` if the start or the
end is blocked.

`paths[r][c] = above + left`, a blocked cell is `0`.

The last grid is 18 × 18; walking every path one by one means billions of
paths, a table is needed.

**Expected output:**

```
6
2
0
2333606220
```
