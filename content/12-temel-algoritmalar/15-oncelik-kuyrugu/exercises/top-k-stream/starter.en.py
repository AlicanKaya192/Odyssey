import heapq


def top_k(stream, k):
    if k <= 0:
        return []
    heap = []
    # A min-heap of size k.

    result = []
    # Empty it and reverse.
    return result


print(top_k([4, 1, 7, 3, 9, 2, 8], 3))
print(top_k([5, 5, 5], 2))
