def decode_grid(output, S, size, threshold):
    return []

empty = [0.0] * 7
grid = [[empty, [0.9, 0.5, 0.5, 0.5, 0.5, 0.1, 0.9]],
        [[0.6, 0.25, 0.75, 0.25, 0.25, 0.7, 0.3], [0.4, 0.5, 0.5, 0.5, 0.5, 1.0, 0.0]]]
for box in decode_grid(grid, 2, 16, 0.4):
    print(box)
