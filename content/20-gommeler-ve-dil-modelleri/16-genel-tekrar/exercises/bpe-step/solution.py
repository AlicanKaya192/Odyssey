from collections import Counter


def bpe_step(words):
    pairs = Counter(p for w in words for p in zip(w, w[1:]))
    if not pairs:
        return words
    top = max(pairs.values())
    a, b = min(p for p, n in pairs.items() if n == top)
    merged = []
    for w in words:
        out, i = [], 0
        while i < len(w):
            if i + 1 < len(w) and w[i] == a and w[i + 1] == b:
                out.append(a + b)
                i += 2
            else:
                out.append(w[i])
                i += 1
        merged.append(out)
    return merged

words = [["l", "o", "w"], ["l", "o", "w", "e", "r"], ["n", "e", "w"]]
words = bpe_step(words)
print([" ".join(w) for w in words])
print([" ".join(w) for w in bpe_step(words)])
