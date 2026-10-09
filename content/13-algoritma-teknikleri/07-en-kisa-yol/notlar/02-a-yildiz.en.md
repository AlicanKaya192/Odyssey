In the lesson we saw A*'s results; here is the code. Its only difference from
Dijkstra is the key put in the heap: `path so far + estimate to the goal`. To
prefer the deeper one on a tie (larger `g`), the second field is `-g`.

```python
import heapq
import math

def astar(grid):
    rows, cols = len(grid), len(grid[0])
    goal = (rows - 1, cols - 1)

    def estimate(r, c):                     # Manhattan: at least this much to the goal
        return abs(r - goal[0]) + abs(c - goal[1])

    best = {(0, 0): 0}
    heap = [(estimate(0, 0), 0, 0, 0)]      # (f, -g, row, col)
    expanded = 0
    while heap:
        f, neg_g, r, c = heapq.heappop(heap)
        g = -neg_g
        if g > best[(r, c)]:
            continue                        # an old record
        expanded += 1
        if (r, c) == goal:
            return g, expanded
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            inside = 0 <= nr < rows and 0 <= nc < cols
            free = inside and grid[nr][nc] == "."
            if free and g + 1 < best.get((nr, nc), math.inf):
                best[(nr, nc)] = g + 1
                heapq.heappush(heap, (g + 1 + estimate(nr, nc), -(g + 1), nr, nc))
    return -1, expanded

grid = ["....#...",
        ".##.#.#.",
        ".#....#.",
        ".#.##.#.",
        "...#..#."]
print(astar(grid))
```

```text
(15, 27)
```

If `estimate` always returned 0, this code would be Dijkstra itself. As long
as the estimate is **admissible** (never exceeds the real distance), the first
time the goal comes out is the shortest path. If diagonal moves are allowed,
Manhattan overestimates; then the Chebyshev or Euclidean distance is used.
