import heapq


def merge_sorted(lists):
    heap = []
    for number, items in enumerate(lists):
        if items:
            heapq.heappush(heap, (items[0], number, 0))
    result = []
    while heap:
        value, number, index = heapq.heappop(heap)
        result.append(value)
        if index + 1 < len(lists[number]):
            heapq.heappush(heap, (lists[number][index + 1], number, index + 1))
    return result


print(merge_sorted([[1, 4, 9], [2, 3, 10], [5]]))
print(merge_sorted([[], [7], [1, 1]]))
