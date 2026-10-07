from collections import defaultdict
from orders_data import make_orders

orders = make_orders(200_000)

without = 0
with_combiner = 0
combined = defaultdict(int)
for i in range(5):
    chunk = orders.iloc[i * 40_000:(i + 1) * 40_000]
    pairs = list(zip(chunk["payment"], chunk["quantity"]))
    without += len(pairs)
    local = defaultdict(int)
    for key, value in pairs:
        local[key] += value
    with_combiner += len(local)
    for key, value in local.items():
        combined[key] += value

print(without, with_combiner)

expected = orders.groupby("payment")["quantity"].sum()
print(all(combined[p] == expected[p] for p in expected.index))
