def linear_search(items, target):
    steps = 0
    for i in range(len(items)):
        steps += 1
        if items[i] == target:
            return i, steps
    return -1, steps


data = [8, 3, 5, 3, 9]
print(linear_search(data, 8))
print(linear_search(data, 3))
print(linear_search(data, 9))
print(linear_search(data, 7))
