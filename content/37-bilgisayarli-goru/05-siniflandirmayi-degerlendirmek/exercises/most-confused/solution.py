def most_confused(matrix):
    best = [0, 0, -1]
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if i != j and value > best[2]:
                best = [i, j, value]
    return best

matrix = [[50, 2, 0], [7, 40, 1], [0, 3, 45]]
print(most_confused(matrix))
