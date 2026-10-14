def error_kinds(predicted, gold):
    right = unknown = wrong = 0
    for p, g in zip(predicted, gold):
        if p == g:
            right += 1
        elif p == "unknown":
            unknown += 1
        else:
            wrong += 1
    return [right, unknown, wrong]


print(error_kinds(["a", "unknown", "b", "c"], ["a", "b", "c", "c"]))
print(error_kinds([], []))
