import numpy as np


def update_weights(w, wrong, alpha):
    w, wrong = np.array(w, dtype=float), np.array(wrong)
    # Yanlislari agirlastir, normallestir.
    return w.round(4).tolist()

w = [0.25, 0.25, 0.25, 0.25]
print(update_weights(w, [False, True, False, False], 1.0986))
