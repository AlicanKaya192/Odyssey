from collections import Counter


def top_contexts(sentences, word, window, k):
    found = Counter()
    for s in sentences:
        for i, w in enumerate(s):
            if w == word:
                left, right = max(0, i - window), min(len(s), i + window + 1)
                found.update(s[j] for j in range(left, right) if j != i)
    ranked = sorted(found.items(), key=lambda item: (-item[1], item[0]))
    return [[w, n] for w, n in ranked[:k]]

sentences = [s.split() for s in ["the cat chased the dog",
                                 "the dog chased the cat",
                                 "a cat sleeps"]]
print(top_contexts(sentences, "cat", 1, 3))
