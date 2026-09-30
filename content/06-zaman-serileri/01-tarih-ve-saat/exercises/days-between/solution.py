from datetime import date

order = date(2024, 2, 27)
delivery = date(2024, 3, 4)

print((delivery - order).days)
print(delivery.strftime("%A"))

order_2023 = date(2023, 2, 27)
delivery_2023 = date(2023, 3, 4)
print((delivery_2023 - order_2023).days)
