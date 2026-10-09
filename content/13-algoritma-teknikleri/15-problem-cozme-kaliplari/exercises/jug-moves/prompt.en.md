Write the function `min_moves(a, b, goal)` with **BFS**: with two empty
buckets of `a` and `b` litres, it returns the fewest moves needed so that one
bucket holds exactly `goal` litres; `-1` if impossible.

Moves: fill one, empty one, pour from one into the other without overflowing.
The state is `(x, y)`; keep the distances in a dictionary.

**Expected output:**

```
6
-1
10
```
