START = {"DET": 0.6, "PRON": 0.4}
TRANS = {"DET": {"DET": 0.0, "NOUN": 0.9, "VERB": 0.1, "PRON": 0.0},
         "PRON": {"DET": 0.0, "NOUN": 0.1, "VERB": 0.9, "PRON": 0.0},
         "VERB": {"DET": 0.8, "NOUN": 0.2, "VERB": 0.0, "PRON": 0.0},
         "NOUN": {"DET": 0.1, "NOUN": 0.1, "VERB": 0.8, "PRON": 0.0}}
EMIT = {"DET": {"the": 1.0}, "PRON": {"i": 1.0},
        "NOUN": {"book": 0.6, "table": 0.4}, "VERB": {"book": 0.5, "read": 0.5}}


def path_prob(words, tags):
    return 0.0

print(path_prob(["i", "book", "the", "table"], ["PRON", "VERB", "DET", "NOUN"]))
print(path_prob(["i", "book", "the", "table"], ["PRON", "NOUN", "DET", "NOUN"]))
