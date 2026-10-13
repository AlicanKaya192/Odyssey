from collections import Counter

TRAIN = [[["the", "DET"], ["book", "NOUN"]], [["i", "PRON"], ["book", "VERB"]],
         [["the", "DET"], ["book", "NOUN"]], [["i", "PRON"], ["run", "VERB"]]]


def emission_prob(train, tag, word, k):
    return 0.0

print(emission_prob(TRAIN, "NOUN", "book", 0))
print(emission_prob(TRAIN, "VERB", "book", 0.5))
print(emission_prob(TRAIN, "VERB", "zebra", 0.5))
