NEGATORS = {"not", "no", "never"}
PUNCT = {".", ",", "!", "?"}


def mark_negation(tokens):
    result, negated = [], False
    for token in tokens:
        if token in PUNCT:
            negated = False
            result.append(token)
        elif token in NEGATORS:
            negated = True
            result.append(token)
        else:
            result.append("NOT_" + token if negated else token)
    return result

tokens = ["it", "is", "not", "good", "at", "all", ".", "love", "it"]
print(" ".join(mark_negation(tokens)))
