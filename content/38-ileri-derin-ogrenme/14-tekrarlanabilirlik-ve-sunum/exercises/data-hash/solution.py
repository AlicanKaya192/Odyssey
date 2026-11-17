import hashlib
import numpy as np


def data_hash(values):
    array = np.ascontiguousarray(np.array(values, dtype=np.float32))
    return hashlib.sha256(array.tobytes()).hexdigest()


def same_data(a, b):
    return data_hash(a) == data_hash(b)

print(same_data([[1.0, 2.0]], [[1.0, 2.0]]))
print(same_data([[1.0, 2.0]], [[1.0, 2.001]]))
