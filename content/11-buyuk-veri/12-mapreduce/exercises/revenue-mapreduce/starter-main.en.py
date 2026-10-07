from collections import defaultdict
from orders_data import make_orders

orders = make_orders(50_000)
rows = orders[["category", "quantity", "unit_price"]].to_dict("records")


def mapper(row):
    # (category, revenue).
    pass


def reducer(key, values):
    # (category, total).
    pass


# Shuffle, reduce, the top three, the pandas comparison.
