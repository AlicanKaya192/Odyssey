from orders_data import make_orders

df = make_orders(1_000_000)
prices = df["unit_price"]

real = prices.sum()
as_float32 = float(prices.astype("float32").sum())
cents = (prices * 100).round().astype("int64")
as_cents = cents.sum() / 100

print(round(real, 2))
print(round(as_float32, 2))
print(round(as_cents, 2))
print(round(as_float32 - real, 2), round(as_cents - real, 2))
