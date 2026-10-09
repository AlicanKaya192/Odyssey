def pair_with_sum(items, target):
    left, right = 0, len(items) - 1
    while left < right:
        total = items[left] + items[right]
        if total == target:
            return items[left], items[right]
        if total < target:
            left += 1
        else:
            right -= 1
    return None


print(pair_with_sum([1, 3, 4, 6, 9], 7))
print(pair_with_sum([1, 3, 4, 6, 9], 14))
evens = list(range(0, 400_000, 2))
print(pair_with_sum(evens, 7))
