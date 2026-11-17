import hashlib
import numpy as np


def data_hash(values):
    # float32 dizinin baytlarindan SHA-256 ozeti
    return ""


def same_data(a, b):
    return data_hash(a) == data_hash(b)

print(same_data([[1.0, 2.0]], [[1.0, 2.0]]))
print(same_data([[1.0, 2.0]], [[1.0, 2.001]]))
