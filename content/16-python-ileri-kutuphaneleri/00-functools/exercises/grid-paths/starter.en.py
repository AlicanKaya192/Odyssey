from functools import lru_cache


def grid_paths(rows, cols):
    if rows == 1 or cols == 1:
        return 1
    return grid_paths(rows - 1, cols) + grid_paths(rows, cols - 1)

print(grid_paths(3, 3))
print(grid_paths(16, 16))
