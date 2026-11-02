import numpy as np
from ab_data import make_population

users = make_population()
true_p = users["bought"].mean()
sample = users["bought"].sample(n=1000, random_state=32)
p_hat = sample.mean()
se = np.sqrt(p_hat * (1 - p_hat) / len(sample))
print(round(p_hat, 4))
print(round(se, 4))
print(round((p_hat - true_p) / se, 2))
