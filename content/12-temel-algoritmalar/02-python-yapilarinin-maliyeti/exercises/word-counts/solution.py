def word_counts(words):
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


print(word_counts(["to", "be", "or", "not", "to", "be"]))
print(word_counts([]))
