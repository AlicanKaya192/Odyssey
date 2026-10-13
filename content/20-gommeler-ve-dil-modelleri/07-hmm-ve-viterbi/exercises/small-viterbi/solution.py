START = {"DET": 0.6, "PRON": 0.4}
TRANS = {"DET": {"DET": 0.0, "NOUN": 0.9, "VERB": 0.1, "PRON": 0.0},
         "PRON": {"DET": 0.0, "NOUN": 0.1, "VERB": 0.9, "PRON": 0.0},
         "VERB": {"DET": 0.8, "NOUN": 0.2, "VERB": 0.0, "PRON": 0.0},
         "NOUN": {"DET": 0.1, "NOUN": 0.1, "VERB": 0.8, "PRON": 0.0}}
EMIT = {"DET": {"the": 1.0}, "PRON": {"i": 1.0},
        "NOUN": {"book": 0.6, "table": 0.4}, "VERB": {"book": 0.5, "read": 0.5}}

TAGS = list(TRANS)


def viterbi(words):
    best = {t: (START.get(t, 0.0) * EMIT[t].get(words[0], 0.0), [t]) for t in TAGS}
    for word in words[1:]:
        new = {}
        for t in TAGS:
            score, path = max((best[p][0] * TRANS[p].get(t, 0.0), best[p][1]) for p in TAGS)
            new[t] = (score * EMIT[t].get(word, 0.0), path + [t])
        best = new
    return max(best.values())[1]

print(viterbi(["i", "book", "the", "table"]))
print(viterbi(["the", "book"]))
