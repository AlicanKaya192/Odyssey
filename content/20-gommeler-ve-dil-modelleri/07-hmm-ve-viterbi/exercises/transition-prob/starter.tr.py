from collections import Counter

TRAIN = [[["the", "DET"], ["book", "NOUN"]], [["i", "PRON"], ["book", "VERB"]],
         [["the", "DET"], ["book", "NOUN"]], [["i", "PRON"], ["run", "VERB"]]]


def transition_prob(train, a, b):
    return 0.0

print(transition_prob(TRAIN, "<s>", "DET"))
print(transition_prob(TRAIN, "PRON", "VERB"))
print(transition_prob(TRAIN, "DET", "VERB"))
