from collections import Counter


def top_pairs(words, k):
    pairs = Counter()
    for symbols, n in words:
        for a, b in zip(symbols, symbols[1:]):
            pairs[a, b] += n
    ranked = sorted(pairs.items(), key=lambda item: (-item[1], item[0]))
    return [[a, b, n] for (a, b), n in ranked[:k]]

words = [[["l", "o", "w", "</w>"], 5], [["l", "o", "w", "e", "r", "</w>"], 2],
         [["n", "e", "w", "</w>"], 6]]
for row in top_pairs(words, 3):
    print(row)
