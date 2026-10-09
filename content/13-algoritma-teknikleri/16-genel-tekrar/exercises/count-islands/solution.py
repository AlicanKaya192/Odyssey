from collections import deque


def count_islands(grid):
    seen = set()
    islands = 0
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1" or (r, c) in seen:
                continue
            islands += 1
            seen.add((r, c))
            queue = deque([(r, c)])
            while queue:
                y, x = queue.popleft()
                for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                    inside = 0 <= ny < rows and 0 <= nx < cols
                    if inside and grid[ny][nx] == "1" and (ny, nx) not in seen:
                        seen.add((ny, nx))
                        queue.append((ny, nx))
    return islands

grid = ["11000",
        "11010",
        "00011",
        "10000"]
print(count_islands(grid))
print(count_islands(["000", "000"]))
big = ["10" * 150 if r % 2 == 0 else "0" * 300 for r in range(300)]
print(count_islands(big))
