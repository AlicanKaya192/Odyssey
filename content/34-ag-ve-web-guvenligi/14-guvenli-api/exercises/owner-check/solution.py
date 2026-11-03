def get_order(orders, user, order_id):
    for order in orders:
        if order["id"] == order_id and order["owner"] == user:
            return order
    return None

ORDERS = [
    {"id": 1, "owner": "ada", "total": 40},
    {"id": 2, "owner": "bob", "total": 75},
]
print(get_order(ORDERS, "ada", 1))
print(get_order(ORDERS, "ada", 2))
print(get_order(ORDERS, "ada", 9))
