NEGATORS = {"not", "no", "never"}
PUNCT = {".", ",", "!", "?"}


def mark_negation(tokens):
    return tokens

tokens = ["it", "is", "not", "good", "at", "all", ".", "love", "it"]
print(" ".join(mark_negation(tokens)))
