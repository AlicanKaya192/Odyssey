def error_kinds(predicted, gold):
    return [0, 0, 0]


print(error_kinds(["a", "unknown", "b", "c"], ["a", "b", "c", "c"]))
print(error_kinds([], []))
