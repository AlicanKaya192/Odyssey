import random


def sort_and_count(items):
    if len(items) <= 1:
        return items, 0
    mid = len(items) // 2
    left, a = sort_and_count(items[:mid])
    right, b = sort_and_count(items[mid:])
    merged = []
    count = 0
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            count += len(left) - i
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, a + b + count


print(sort_and_count([2, 4, 1, 3, 5]))
print(sort_and_count([5, 4, 3, 2, 1]))
random.seed(7)
data = random.sample(range(50_000), 50_000)
print(sort_and_count(data)[1])
