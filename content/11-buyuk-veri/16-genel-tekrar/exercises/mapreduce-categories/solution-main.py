import zlib
from orders_data import make_orders

orders = make_orders(100_000)
orders["revenue"] = orders["quantity"] * orders["unit_price"]
machines = [orders.iloc[i * 25_000:(i + 1) * 25_000] for i in range(4)]

combined = []
for machine in machines:
    local = {}
    for category, revenue in zip(machine["category"], machine["revenue"]):
        local[category] = local.get(category, 0.0) + revenue
    combined.append(local)

reducers = [{}, {}]
sent = 0
for local in combined:
    for key, value in local.items():
        target = zlib.crc32(key.encode()) % 2
        reducers[target].setdefault(key, []).append(value)
        sent += 1

result = {}
for reducer in reducers:
    for key, values in reducer.items():
        result[key] = sum(values)

print(sent)
for number, reducer in enumerate(reducers):
    print(number, " ".join(sorted(reducer)))
expected = orders.groupby("category")["revenue"].sum()
print(all(abs(result[key] - expected[key]) < 0.01 for key in expected.index))
