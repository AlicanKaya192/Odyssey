from collections import Counter

SENTENCES = [["my", "order", "is", "late"], ["my", "card", "was", "charged"],
             ["my", "order", "never", "came"], ["the", "order", "is", "late"]]


def next_word(sentences, word):
    return ""

print(next_word(SENTENCES, "my"))
print(next_word(SENTENCES, "order"))
print(next_word(SENTENCES, "<s>"))
