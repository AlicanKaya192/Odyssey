import heapq


def top_words(words, k):
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return heapq.nsmallest(k, counts, key=lambda w: (-counts[w], w))


text = "the cat and the dog and the bird saw a cat"
print(top_words(text.split(), 3))
print(top_words(["b", "a", "b", "a", "c"], 2))
