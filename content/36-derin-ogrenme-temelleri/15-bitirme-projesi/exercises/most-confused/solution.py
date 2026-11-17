def most_confused(matrix):
    best = [0, 0, -1]
    for t, row in enumerate(matrix):
        for p, count in enumerate(row):
            if t != p and count > best[2]:
                best = [t, p, count]
    return best

print(most_confused([[5, 1, 0], [0, 4, 3], [2, 0, 6]]))
