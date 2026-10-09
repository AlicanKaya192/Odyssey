import heapq
from collections import Counter


def huffman_bits(text):
    counts = list(Counter(text).values())
    if len(counts) <= 1:
        return len(text)
    # Heap'e koy, en kucuk iki sayiyi birlestir.
    return 0


print(huffman_bits("abracadabra"))
print(huffman_bits("mississippi"))
print(huffman_bits("aaaa"))
