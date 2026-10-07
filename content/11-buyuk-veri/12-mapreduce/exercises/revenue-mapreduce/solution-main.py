from collections import defaultdict
from orders_data import make_orders

orders = make_orders(50_000)
rows = orders[["category", "quantity", "unit_price"]].to_dict("records")


def mapper(row):
    yield row["category"], row["quantity"] * row["unit_price"]


def reducer(key, values):
    return key, sum(values)


groups = defaultdict(list)
for row in rows:
    for key, value in mapper(row):
        groups[key].append(value)
result = dict(reducer(k, v) for k, v in groups.items())

top = sorted(result.items(), key=lambda kv: -kv[1])[:3]
for category, revenue in top:
    print(category, round(revenue / 1e6, 2))

expected = (orders["quantity"] * orders["unit_price"]).groupby(orders["category"]).sum()
print(all(abs(result[c] - expected[c]) < 0.01 for c in expected.index))
