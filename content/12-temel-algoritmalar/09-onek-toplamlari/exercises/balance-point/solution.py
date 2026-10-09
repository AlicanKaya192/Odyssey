def balance_index(values):
    total = sum(values)
    left = 0
    for i, x in enumerate(values):
        right = total - left - x
        if left == right:
            return i
        left += x
    return -1


print(balance_index([1, 7, 3, 6, 5, 6]))
print(balance_index([1, 2, 3]))
print(balance_index([2, 1, -1]))
