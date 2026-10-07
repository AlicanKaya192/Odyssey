import zlib
from orders_data import make_orders

orders = make_orders(100_000)
orders["revenue"] = orders["quantity"] * orders["unit_price"]
machines = [orders.iloc[i * 25_000:(i + 1) * 25_000] for i in range(4)]

# 2. Map + combiner.


# 3. Shuffle.
reducers = [{}, {}]


# 4. Reduce and 5. the results.
