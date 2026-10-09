import numpy as np


def majority_vote(predictions):
    P = np.array(predictions)
    # The mean per column.
    return []

preds = [[1, 0, 1, 0], [1, 1, 0, 0], [0, 1, 1, 0]]
print(majority_vote(preds))
