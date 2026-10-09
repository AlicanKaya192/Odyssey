from collections import deque


def count_islands(grid):
    rows, cols = len(grid), len(grid[0])
    seen = set()
    islands = 0
    # A walk from every new land cell.
    return islands


print(count_islands(["##..", "#..#", "..##", "#..."]))
print(count_islands(["...", "..."]))
big = ["".join("#" if (r // 3 + c // 3) % 7 != 0 else "." for c in range(400)) for r in range(400)]
print(count_islands(big))
