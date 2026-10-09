def sort_by_score(records):
    if len(records) <= 1:
        return records
    mid = len(records) // 2
    left = sort_by_score(records[:mid])
    right = sort_by_score(records[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][1] <= right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


print(sort_by_score([["Bora", 2], ["Ada", 2], ["Cem", 1]]))
print(sort_by_score([["x", 5], ["y", 3], ["z", 5], ["w", 3]]))
