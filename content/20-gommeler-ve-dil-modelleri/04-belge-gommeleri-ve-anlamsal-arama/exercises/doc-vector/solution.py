import numpy as np


def doc_vector(tokens, table):
    known = [table[t] for t in tokens if t in table]
    if not known:
        return [0.0, 0.0]
    v = np.mean(known, axis=0)
    return (v / np.linalg.norm(v)).round(3).tolist()

table = {"parcel": [1.0, 0.0], "box": [0.6, 0.8], "password": [0.0, 1.0]}
print(doc_vector("the parcel box".split(), table))
print(doc_vector("hello".split(), table))
