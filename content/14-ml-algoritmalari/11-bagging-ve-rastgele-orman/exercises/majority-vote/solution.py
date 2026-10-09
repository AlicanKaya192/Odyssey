import numpy as np


def majority_vote(predictions):
    P = np.array(predictions)
    return (P.mean(axis=0) > 0.5).astype(int).tolist()

preds = [[1, 0, 1, 0], [1, 1, 0, 0], [0, 1, 1, 0]]
print(majority_vote(preds))
