def make_grid(rows, cols, fill):
    return [[fill] * cols] * rows

grid = make_grid(2, 3, 0)
grid[0][1] = 5
print(grid)
