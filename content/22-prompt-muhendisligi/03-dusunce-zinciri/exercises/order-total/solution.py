def order_total(items, discount, fee, free_over):
    subtotal = sum(price * count for price, count in items)
    total = subtotal * (1 - discount)
    if total < free_over:
        total += fee
    return round(total, 2)


print(order_total([[189.90, 1], [12.50, 2]], 0.10, 4.90, 50))
print(order_total([[12.50, 2]], 0.0, 4.90, 50))
