Write the function `maze_steps(maze)`: `maze` is a list of strings, `.` is
empty, `#` a wall. It returns **the fewest steps** from the top-left to the
bottom-right moving in four directions (up, down, right, left); `-1` if it
cannot be reached.

Keep `(row, col, steps)` in the queue; add to `seen` when entering. The last
line has a 300 × 300 maze.

**Expected output:**

```
4
-1
598
```
