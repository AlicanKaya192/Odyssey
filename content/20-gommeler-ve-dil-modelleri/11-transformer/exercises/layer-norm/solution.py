import math


def layer_norm(rows):
    result = []
    for row in rows:
        mean = sum(row) / len(row)
        var = sum((x - mean) ** 2 for x in row) / len(row)
        result.append([round((x - mean) / math.sqrt(var + 1e-5), 3) for x in row])
    return result

for row in layer_norm([[1.0, 2.0, 3.0], [5.0, 5.0, 8.0]]):
    print(row)
