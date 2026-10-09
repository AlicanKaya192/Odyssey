def longest_k_distinct(text, k):
    counts = {}
    start = 0
    best = 0
    for end, ch in enumerate(text):
        counts[ch] = counts.get(ch, 0) + 1
        while len(counts) > k:
            left = text[start]
            counts[left] -= 1
            if counts[left] == 0:
                del counts[left]
            start += 1
        best = max(best, end - start + 1)
    return best


print(longest_k_distinct("eceba", 2))
print(longest_k_distinct("aaabbcc", 2))
print(longest_k_distinct("abc", 0))
