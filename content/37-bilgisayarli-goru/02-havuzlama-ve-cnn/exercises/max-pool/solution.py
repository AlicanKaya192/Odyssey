def max_pool(fmap, size):
    out = []
    for r in range(0, len(fmap) - size + 1, size):
        row = []
        for c in range(0, len(fmap[0]) - size + 1, size):
            window = [fmap[r + i][c + j] for i in range(size) for j in range(size)]
            row.append(max(window))
        out.append(row)
    return out

fmap = [[1, 3, 2, 0], [4, 6, 1, 1], [0, 2, 9, 5], [1, 1, 3, 7]]
print(max_pool(fmap, 2))
print(max_pool([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2))
