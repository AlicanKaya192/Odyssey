from collections import Counter

SENTENCES = [["my", "order", "is", "late"], ["my", "card", "was", "charged"],
             ["my", "order", "never", "came"], ["the", "order", "is", "late"]]


def next_word(sentences, word):
    padded = [["<s>"] + s + ["</s>"] for s in sentences]
    after = Counter(b for s in padded for a, b in zip(s, s[1:]) if a == word)
    return min(after, key=lambda w: (-after[w], w))

print(next_word(SENTENCES, "my"))
print(next_word(SENTENCES, "order"))
print(next_word(SENTENCES, "<s>"))
