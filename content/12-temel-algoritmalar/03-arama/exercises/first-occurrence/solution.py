def first_occurrence(items, target):
    lo, hi = 0, len(items) - 1
    answer = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            answer = mid
            hi = mid - 1
        elif items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return answer


scores = [40, 55, 55, 55, 70, 70, 90]
print(first_occurrence(scores, 55))
print(first_occurrence(scores, 70))
print(first_occurrence(scores, 60))
