import tracemalloc
import numpy as np

tracemalloc.start()
prices = np.ones(2_000_000)
taxed = prices * 1.2
final = np.round(taxed, 2)
first_peak = tracemalloc.get_traced_memory()[1]
tracemalloc.stop()

del prices, taxed, final

tracemalloc.start()
prices = np.ones(2_000_000)
prices *= 1.2
np.round(prices, 2, out=prices)
second_peak = tracemalloc.get_traced_memory()[1]
tracemalloc.stop()

print(round(first_peak / 1024**2, 1))
print(round(second_peak / 1024**2, 1))
print(round(first_peak / second_peak))
