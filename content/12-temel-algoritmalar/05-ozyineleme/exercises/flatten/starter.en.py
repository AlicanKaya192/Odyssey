def flatten(items):
    result = []
    # Each element: if it is a list, add flatten(element)'s result, otherwise itself.

    return result


print(flatten([1, [2, 3], [4, [5, [6]]]]))
print(flatten([[], [[]]]))
