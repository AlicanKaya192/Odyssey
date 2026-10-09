def grid_paths(grid):
    rows, cols = len(grid), len(grid[0])
    paths = [[0] * cols for _ in range(rows)]
    # Satir satir doldur: ust + sol, engel 0.
    return paths[-1][-1]


print(grid_paths(["...", "...", "..."]))
print(grid_paths(["...", ".#.", "..."]))
print(grid_paths([".#", "#."]))
big = ["." * 18 for _ in range(18)]
print(grid_paths(big))
