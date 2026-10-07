from orders_data import make_orders

df = make_orders(50_000)

by_order = df.set_index("order_id")
by_customer = df.set_index("customer_id")

for table in [df, by_order, by_customer]:
    print(type(table.index).__name__, table.memory_usage(deep=True)["Index"])

print(round(by_customer.memory_usage(deep=True).sum() / 1024**2, 1))
