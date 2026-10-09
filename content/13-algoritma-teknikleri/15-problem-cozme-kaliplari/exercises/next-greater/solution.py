def next_greater(values):
    result = [-1] * len(values)
    stack = []
    for i, v in enumerate(values):
        while stack and values[stack[-1]] < v:
            result[stack.pop()] = v
        stack.append(i)
    return result

print(next_greater([4, 1, 3, 2, 5]))
print(next_greater([7, 7, 7]))
falling = list(range(100_000, 0, -1))
print(next_greater(falling)[-3:])
