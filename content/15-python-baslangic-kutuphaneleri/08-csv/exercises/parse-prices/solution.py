import csv


def parse_prices(path):
    prices = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f, delimiter=";"):
            prices[row["product"]] = float(row["price"].replace(",", "."))
    return prices

prices = parse_prices("prices.csv")
for name in sorted(prices):
    print(name, prices[name])
