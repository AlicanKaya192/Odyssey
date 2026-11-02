import numpy as np
from ab_data import make_population

users = make_population()
true_p = users["bought"].mean()
sample = users["bought"].sample(n=1000, random_state=32)
# 1) Print the share in the sample (p_hat) with 4 places.
# 2) Print its standard error sqrt(p_hat * (1 - p_hat) / n) with 4 places.
# 3) Print how many standard errors the estimate is from the truth
#    ((p_hat - true_p) / se) with 2 places.
