def flatten(items):
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


print(flatten([1, [2, 3], [4, [5, [6]]]]))
print(flatten([[], [[]]]))
