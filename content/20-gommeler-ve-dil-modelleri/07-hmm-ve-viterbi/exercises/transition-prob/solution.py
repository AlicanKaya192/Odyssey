from collections import Counter

TRAIN = [[["the", "DET"], ["book", "NOUN"]], [["i", "PRON"], ["book", "VERB"]],
         [["the", "DET"], ["book", "NOUN"]], [["i", "PRON"], ["run", "VERB"]]]


def transition_prob(train, a, b):
    pairs, starts = Counter(), Counter()
    for s in train:
        tags = ["<s>"] + [t for _, t in s]
        for x, y in zip(tags, tags[1:]):
            pairs[x, y] += 1
            starts[x] += 1
    return round(pairs[a, b] / starts[a], 3) if starts[a] else 0.0

print(transition_prob(TRAIN, "<s>", "DET"))
print(transition_prob(TRAIN, "PRON", "VERB"))
print(transition_prob(TRAIN, "DET", "VERB"))
