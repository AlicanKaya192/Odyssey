def next_greater(values):
    result = [-1] * len(values)
    stack = []
    for i, x in enumerate(values):
        while stack and values[stack[-1]] < x:
            result[stack.pop()] = x
        stack.append(i)
    return result


print(next_greater([2, 7, 3, 5, 4, 6, 8]))
temps = list(range(200_000, 0, -1))
print(next_greater(temps).count(-1))
