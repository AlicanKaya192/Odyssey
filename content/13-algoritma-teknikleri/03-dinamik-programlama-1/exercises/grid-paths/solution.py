def grid_paths(grid):
    rows, cols = len(grid), len(grid[0])
    paths = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "#":
                continue
            if r == 0 and c == 0:
                paths[r][c] = 1
            else:
                up = paths[r - 1][c] if r else 0
                left = paths[r][c - 1] if c else 0
                paths[r][c] = up + left
    return paths[-1][-1]


print(grid_paths(["...", "...", "..."]))
print(grid_paths(["...", ".#.", "..."]))
print(grid_paths([".#", "#."]))
big = ["." * 18 for _ in range(18)]
print(grid_paths(big))
