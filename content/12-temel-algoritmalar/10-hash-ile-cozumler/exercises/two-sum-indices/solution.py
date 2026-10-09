def two_sum(numbers, target):
    seen = {}
    for i, x in enumerate(numbers):
        if target - x in seen:
            return seen[target - x], i
        seen[x] = i
    return None


print(two_sum([8, 3, 11, 5, 7], 12))
print(two_sum([3, 3], 6))
big = list(range(0, 400_000, 2))
print(two_sum(big, 1))
