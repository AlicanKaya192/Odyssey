import math


def analogy(vectors, a, b, c):
    target = [y - x + z for x, y, z in zip(vectors[a], vectors[b], vectors[c])]
    norm_t = math.sqrt(sum(t * t for t in target))
    best, best_sim = None, -2.0
    for word, v in vectors.items():
        if word in (a, b, c):
            continue
        dot = sum(t * x for t, x in zip(target, v))
        sim = dot / (norm_t * math.sqrt(sum(x * x for x in v)))
        if sim > best_sim:
            best, best_sim = word, sim
    return best

vectors = {"king": [1.0, 1.0], "man": [1.0, 0.0], "woman": [0.0, 1.0],
           "queen": [0.1, 2.0], "prince": [1.0, 0.5]}
print(analogy(vectors, "man", "king", "woman"))
print(analogy(vectors, "woman", "queen", "man"))
