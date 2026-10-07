from collections import defaultdict
from orders_data import make_orders

orders = make_orders(50_000)
rows = orders[["category", "quantity", "unit_price"]].to_dict("records")


def mapper(row):
    # (kategori, ciro).
    pass


def reducer(key, values):
    # (kategori, toplam).
    pass


# Shuffle, reduce, ilk uc, pandas karsilastirmasi.
