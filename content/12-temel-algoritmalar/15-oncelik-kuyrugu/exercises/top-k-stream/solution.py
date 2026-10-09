import heapq


def top_k(stream, k):
    if k <= 0:
        return []
    heap = []
    for x in stream:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)
    result = []
    while heap:
        result.append(heapq.heappop(heap))
    result.reverse()
    return result


print(top_k([4, 1, 7, 3, 9, 2, 8], 3))
print(top_k([5, 5, 5], 2))
