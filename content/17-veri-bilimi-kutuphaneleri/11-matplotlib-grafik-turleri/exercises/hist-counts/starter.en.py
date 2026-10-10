import matplotlib.pyplot as plt
import numpy as np


def hist_counts(a, b, bins, low, high):
    fig, ax = plt.subplots()
    counts_a, _, _ = ax.hist(a, bins=bins, alpha=0.6)
    counts_b, _, _ = ax.hist(b, bins=bins, alpha=0.6)
    plt.close(fig)
    return [[int(c) for c in counts_a], [int(c) for c in counts_b]]

A = [12, 25, 31, 33, 38, 44, 51]
B = [30, 41, 45, 48, 55, 62, 70, 79]
counts_a, counts_b = hist_counts(A, B, 4, 0, 80)
print(counts_a)
print(counts_b)
