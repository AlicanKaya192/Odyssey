import numpy as np
from orders_data import make_orders

orders = make_orders(200_000)

spreads = {}
for n in [200, 2_000, 20_000]:
    means = [orders["unit_price"].sample(n=n, random_state=i).mean() for i in range(100)]
    spreads[n] = np.std(means)
    print(n, round(spreads[n], 2))

print(round(spreads[200] / spreads[20_000], 1))
