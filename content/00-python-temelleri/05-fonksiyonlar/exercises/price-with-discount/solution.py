def total_price(price, count, discount=0):
    return price * count - discount


full = total_price(50, 3)
reduced = total_price(50, 3, 20)

print(full)
print(reduced)
