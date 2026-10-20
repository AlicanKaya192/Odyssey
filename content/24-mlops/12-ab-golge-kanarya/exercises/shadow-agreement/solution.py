def agreement(served, shadow):
    same = sum(1 for a, b in zip(served, shadow) if a == b)
    return round(same / len(served), 3)


print(agreement([1, 0, 1, 1], [1, 0, 0, 1]))
print(agreement([0, 0, 0], [0, 0, 0]))
print(agreement([1, 1, 0], [0, 0, 1]))
