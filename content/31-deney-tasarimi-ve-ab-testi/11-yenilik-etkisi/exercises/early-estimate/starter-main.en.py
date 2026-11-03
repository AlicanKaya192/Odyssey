import numpy as np
from ab_data import make_novelty_test
# Build 20 tests with make_novelty_test(n=10000, seed=s), s = 200..219.
# In each compute two relative lifts (B / A - 1):
#   new users' week 1, existing users' week 4.
# Print their averages over the 20 tests on one line with 3 places.
# Week: (day - 1) // 7 + 1.
