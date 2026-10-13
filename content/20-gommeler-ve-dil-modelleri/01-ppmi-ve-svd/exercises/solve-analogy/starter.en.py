import numpy as np


def analogy(vectors, a, b, c):
    return ""

vectors = {"man": [1, 0], "woman": [1, 1], "king": [3, 0],
           "queen": [3, 1], "apple": [0, 2]}
print(analogy(vectors, "man", "king", "woman"))
print(analogy(vectors, "king", "man", "queen"))
