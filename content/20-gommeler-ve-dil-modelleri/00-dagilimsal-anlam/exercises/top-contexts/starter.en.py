from collections import Counter


def top_contexts(sentences, word, window, k):
    return []

sentences = [s.split() for s in ["the cat chased the dog",
                                 "the dog chased the cat",
                                 "a cat sleeps"]]
print(top_contexts(sentences, "cat", 1, 3))
