def binary_search(items, target):
    lo, hi = 0, len(items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


data = [3, 9, 14, 20, 27, 31, 40]
print(binary_search(data, 27))
print(binary_search(data, 3))
print(binary_search(data, 15))
