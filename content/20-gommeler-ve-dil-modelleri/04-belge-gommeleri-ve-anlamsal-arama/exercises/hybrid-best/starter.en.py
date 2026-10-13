import numpy as np


def hybrid_best(lexical, semantic, alpha):
    return []

lexical = [[0.0, 0.8, 0.1], [0.0, 0.0, 0.0]]
semantic = [[0.5, 0.2, 0.6], [0.3, 0.7, 0.1]]
for alpha in [0.0, 0.5, 1.0]:
    print(alpha, hybrid_best(lexical, semantic, alpha))
