from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    quantity: int = 1

    def total(self) -> float:
        return self.price * self.quantity


def order_total(rows):
    products = [Product(*row) for row in rows]
    return round(sum(p.total() for p in products), 2)

print(Product("pen", 1.5, 4))
print(order_total([["pen", 1.5, 4], ["book", 12.0, 1]]))
