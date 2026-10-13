from collections import Counter

TRAIN = [[["the", "DET"], ["book", "NOUN"]], [["i", "PRON"], ["book", "VERB"]],
         [["the", "DET"], ["book", "NOUN"]], [["i", "PRON"], ["run", "VERB"]]]


def baseline_tags(train, words):
    pairs = Counter((w, t) for s in train for w, t in s)
    out = []
    for word in words:
        seen = {t: n for (w, t), n in pairs.items() if w == word}
        out.append(max(sorted(seen), key=seen.get) if seen else "NOUN")
    return out

print(baseline_tags(TRAIN, ["the", "book", "zebra"]))
