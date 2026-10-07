import json

with open("orders.json", encoding="utf-8") as file:
    data = json.load(file)

print(data["shop"])

totals = {}
for order in data["orders"]:
    total = 0
    for item in order["items"]:
        total += item["price"] * item["qty"]
    totals[order["customer"]] = total
    print(order["customer"], total)

print(sum(totals.values()))
