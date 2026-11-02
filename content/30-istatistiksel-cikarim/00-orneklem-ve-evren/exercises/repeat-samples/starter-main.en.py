import numpy as np
from ab_data import make_population

users = make_population()
true_mean = users["minutes"].mean()
sample = users["minutes"].sample(n=50, random_state=0)
print(round(sample.mean(), 2))
# One sample is not enough: repeat this for seeds 0..499, collect the
# means in a list and print the smallest, the largest and the share
# within 1 minute of the truth.
