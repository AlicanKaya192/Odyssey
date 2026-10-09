def reversed_copy(items):
    result = []
    for i in range(len(items) - 1, -1, -1):
        result.append(items[i])
    return result


original = [1, 2, 3, 4]
print(reversed_copy(original))
print(original)
print(reversed_copy([]))
