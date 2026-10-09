def radix_sort(items):
    if not items:
        return items
    place = 1
    largest = max(items)
    while largest // place > 0:
        buckets = [[] for _ in range(10)]
        for x in items:
            buckets[(x // place) % 10].append(x)
        items = [x for bucket in buckets for x in bucket]
        place *= 10
    return items


print(radix_sort([170, 45, 75, 90, 802, 24, 2, 66]))
print(radix_sort([5, 3, 5, 1]))
