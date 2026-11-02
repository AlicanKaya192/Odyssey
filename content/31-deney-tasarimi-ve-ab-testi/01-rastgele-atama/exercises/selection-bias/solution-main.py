import numpy as np
from ab_data import make_user_log

users = make_user_log(n=10000, seed=722)
rng = np.random.default_rng(723)
opted = rng.random(len(users)) < np.clip(0.05 * users["sessions"], 0, 0.9)
print(round(users["bought"][opted].mean(), 4))
print(round(users["bought"][~opted].mean(), 4))
print(round(users["sessions"][opted].mean(), 2))
print(round(users["sessions"][~opted].mean(), 2))
