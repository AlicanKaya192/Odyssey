import numpy as np


def hybrid_best(lexical, semantic, alpha):
    mixed = alpha * np.array(lexical) + (1 - alpha) * np.array(semantic)
    return [int(i) for i in mixed.argmax(axis=1)]

lexical = [[0.0, 0.8, 0.1], [0.0, 0.0, 0.0]]
semantic = [[0.5, 0.2, 0.6], [0.3, 0.7, 0.1]]
for alpha in [0.0, 0.5, 1.0]:
    print(alpha, hybrid_best(lexical, semantic, alpha))
