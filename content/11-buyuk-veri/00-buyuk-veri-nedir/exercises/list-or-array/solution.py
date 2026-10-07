import sys
import numpy as np

values = [i * 0.5 for i in range(100_000)]
array = np.arange(100_000) * 0.5

list_bytes = sys.getsizeof(values) + sum(sys.getsizeof(x) for x in values)
array_bytes = array.nbytes

print(round(list_bytes / 1024**2, 1), round(array_bytes / 1024**2, 1))
print(round(list_bytes / array_bytes, 1))
