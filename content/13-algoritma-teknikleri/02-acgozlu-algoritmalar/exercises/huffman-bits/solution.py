import heapq
from collections import Counter


def huffman_bits(text):
    counts = list(Counter(text).values())
    if len(counts) <= 1:
        return len(text)
    heapq.heapify(counts)
    bits = 0
    while len(counts) > 1:
        first = heapq.heappop(counts)
        second = heapq.heappop(counts)
        bits += first + second
        heapq.heappush(counts, first + second)
    return bits


print(huffman_bits("abracadabra"))
print(huffman_bits("mississippi"))
print(huffman_bits("aaaa"))
