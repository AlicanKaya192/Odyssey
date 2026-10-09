from dataclasses import dataclass


@dataclass
class Product:
    name: str
    # price, quantity, total()


def order_total(rows):
    return 0.0

print(Product("pen", 1.5, 4))
print(order_total([["pen", 1.5, 4], ["book", 12.0, 1]]))
