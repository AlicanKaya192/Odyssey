import numpy as np


def analogy(vectors, a, b, c):
    unit = {w: np.array(v, dtype=float) / np.linalg.norm(v) for w, v in vectors.items()}
    target = unit[b] - unit[a] + unit[c]
    best, best_sim = "", -np.inf
    for w, v in unit.items():
        if w in (a, b, c):
            continue
        sim = v @ target / np.linalg.norm(target)
        if sim > best_sim:
            best, best_sim = w, sim
    return best

vectors = {"man": [1, 0], "woman": [1, 1], "king": [3, 0],
           "queen": [3, 1], "apple": [0, 2]}
print(analogy(vectors, "man", "king", "woman"))
print(analogy(vectors, "king", "man", "queen"))
