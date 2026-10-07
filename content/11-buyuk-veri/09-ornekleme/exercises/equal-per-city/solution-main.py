from orders_data import make_orders

orders = make_orders(200_000)

true = orders.loc[orders["city"] == "Trabzon", "unit_price"].mean()

errors = {"simple": [], "stratified": []}
for i in range(50):
    simple = orders.sample(n=800, random_state=i)
    stratified = orders.groupby("city", group_keys=False).sample(n=100, random_state=i)
    for name, part in [("simple", simple), ("stratified", stratified)]:
        trabzon = part.loc[part["city"] == "Trabzon", "unit_price"]
        errors[name].append(abs(trabzon.mean() - true))

for name, values in errors.items():
    print(name, round(sum(values) / len(values), 1))
