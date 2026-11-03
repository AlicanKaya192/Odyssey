def copy_bounded(memory, start, size, data):
    result = list(memory)
    for i, value in enumerate(data):
        result[start + i] = value
    return result

memory = [0] * 8 + [85, 83, 69, 82]
result = copy_bounded(memory, 0, 8, [1, 2, 3])
print(result[:8])
print(result[8:])
result = copy_bounded(memory, 0, 8, list(range(1, 13)))
print(result[:8])
print(result[8:])
