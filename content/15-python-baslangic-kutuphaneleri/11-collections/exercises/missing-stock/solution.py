from collections import Counter


def missing_stock(order, stock):
    return dict(Counter(order) - Counter(stock))

order = ["pen", "pen", "ink", "book", "pen"]
stock = ["pen", "ink", "ink", "book"]
print(missing_stock(order, stock))
