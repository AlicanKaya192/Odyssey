import numpy as np
from ab_data import make_segment_test

keys = ["country", "platform", "group"]
# Build 50 tests with make_segment_test(n=20000, seed=s), s = 500..549.
# In each, find the total relative lift and the largest of the 16 segment
# lifts. Print the average of the total lifts first, then the average of
# the largest segment lifts, with 3 places. (The true effect is 0.08 in
# every segment.)
