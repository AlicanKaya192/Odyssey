from orders_data import make_orders

df = make_orders(100_000)

for name in ["order_time", "city", "category", "payment"]:
    column = df[name]
    as_text = column.memory_usage(deep=True) / 1024
    as_category = column.astype("category").memory_usage(deep=True) / 1024
    answer = "yes" if as_category < as_text else "no"
    print(name, column.nunique(), round(as_text, 1), round(as_category, 1), answer)
