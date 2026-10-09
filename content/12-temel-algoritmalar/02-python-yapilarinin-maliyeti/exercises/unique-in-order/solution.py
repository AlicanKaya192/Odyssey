def unique_in_order(items):
    result = []
    seen = set()
    for value in items:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


print(unique_in_order([3, 1, 3, 2, 1]))
data = list(range(50_000)) * 2
print(len(unique_in_order(data)))
