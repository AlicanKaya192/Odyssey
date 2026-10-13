from collections import Counter

TRAIN = [[["the", "DET"], ["book", "NOUN"]], [["i", "PRON"], ["book", "VERB"]],
         [["the", "DET"], ["book", "NOUN"]], [["i", "PRON"], ["run", "VERB"]]]


def baseline_tags(train, words):
    return []

print(baseline_tags(TRAIN, ["the", "book", "zebra"]))
