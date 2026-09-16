order_no = 7
items = [("Keyboard", 1, 450.0), ("Mouse", 2, 175.5), ("Cable", 3, 39.9)]
discount = 0.1

print(f"Order {order_no:03d}")

subtotal = 0.0
for name, count, price in items:
    line = count * price
    subtotal += line
    print(f"{name:<12}{count:>4}{line:>10.2f}")

saving = subtotal * discount
total = subtotal - saving

print(f"{'Subtotal':<16}{subtotal:>10.2f}")
label = f"Discount ({discount:.0%})"
print(f"{label:<16}{-saving:>10.2f}")
print(f"{'Total':<16}{total:>10.2f}")
