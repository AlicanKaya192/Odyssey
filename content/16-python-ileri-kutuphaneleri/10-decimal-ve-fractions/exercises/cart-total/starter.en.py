def cart_total(prices):
    total = 0
    for price in prices:
        total += float(price)
    return str(total)

print(cart_total(["1.10", "2.20"]))
print(cart_total(["19.99", "5.01", "0.10"]))
