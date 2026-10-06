stock = {"apple": 10, "pear": 4, "plum": 0}
orders = [("apple", 3), ("pear", 5), ("plum", 1), ("kiwi", 2), ("apple", 6)]

shortages = {}
unknown = []

for product, amount in orders:
    if product not in stock:
        unknown.append(product)
        print(product + ": unknown product")
    elif stock[product] >= amount:
        stock[product] = stock[product] - amount
        print(product + ": sent", amount)
    else:
        missing = amount - stock[product]
        shortages[product] = missing
        print(product + ": short by", missing)

print("Stock:", stock)
