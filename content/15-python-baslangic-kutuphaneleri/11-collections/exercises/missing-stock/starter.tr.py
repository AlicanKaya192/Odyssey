from collections import Counter


def missing_stock(order, stock):
    # Counter(order) - Counter(stock)
    return {}

order = ["pen", "pen", "ink", "book", "pen"]
stock = ["pen", "ink", "ink", "book"]
print(missing_stock(order, stock))
