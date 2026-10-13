import math


def viterbi(words, start, trans, emit):
    return []

start = {"DET": 0.8, "NOUN": 0.2}
trans = {"DET": {"DET": 0.1, "NOUN": 0.9}, "NOUN": {"DET": 0.4, "NOUN": 0.6}}
emit = {"DET": {"the": 0.9, "dog": 0.1}, "NOUN": {"the": 0.1, "dog": 0.9}}
print(viterbi(["the", "dog"], start, trans, emit))
print(viterbi(["dog", "the", "dog"], start, trans, emit))
