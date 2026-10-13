import numpy as np


def doc_vector(tokens, table):
    return []

table = {"parcel": [1.0, 0.0], "box": [0.6, 0.8], "password": [0.0, 1.0]}
print(doc_vector("the parcel box".split(), table))
print(doc_vector("hello".split(), table))
