import numpy as np
from ab_data import make_population

users = make_population()
x = users.sample(n=200, random_state=31)["minutes"]
se = x.std() / len(x)
print(round(x.mean(), 2))
print(round(x.std(), 2))
print(round(se, 3))
