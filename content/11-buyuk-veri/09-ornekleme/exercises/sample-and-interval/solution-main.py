import numpy as np
from orders_data import make_orders

orders = make_orders(200_000)

true_mean = orders["unit_price"].mean()
print(round(true_mean, 2))

sample = orders["unit_price"].sample(n=5_000, random_state=1)
est = sample.mean()
print(round(est, 2))

se = sample.std() / np.sqrt(len(sample))
print(round(se, 2))

low, high = est - 1.96 * se, est + 1.96 * se
print(round(low, 2), round(high, 2))
print(low <= true_mean <= high)
