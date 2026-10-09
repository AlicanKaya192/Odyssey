import heapq


def k_smallest(values, k):
    heap = values[:]
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(min(k, len(heap)))]


nums = [7, 2, 9, 4, 1, 8]
print(k_smallest(nums, 3))
print(k_smallest(nums, 10))
print(nums)
