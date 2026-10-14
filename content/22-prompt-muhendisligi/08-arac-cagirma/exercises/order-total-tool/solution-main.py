from shop_data import ORDERS


def order_total(order_id):
    order = ORDERS.get(order_id)
    if order is None:
        return {"error": f"no order {order_id}"}
    total = sum(price * count for _, price, count in order["items"])
    return {"order_id": order_id, "total": round(total, 2)}


for order_id in ["ORD-10077", "ORD-61890", "ORD-00000"]:
    print(order_total(order_id))
