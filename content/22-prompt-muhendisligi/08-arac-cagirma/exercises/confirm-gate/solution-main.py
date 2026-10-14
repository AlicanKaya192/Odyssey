from shop_data import ORDERS


def get_order(order_id):
    order = ORDERS.get(order_id)
    if order is None:
        return {"error": f"no order {order_id}"}
    return {"order_id": order_id, "status": order["status"]}


def cancel_order(order_id):
    return {"order_id": order_id, "cancelled": True}


TOOLS = {"get_order": {"function": get_order, "confirm": False},
         "cancel_order": {"function": cancel_order, "confirm": True}}


def dispatch(call, confirmed):
    tool = TOOLS.get(call["name"])
    if tool is None:
        return {"error": f"unknown tool {call['name']}"}
    if tool["confirm"] and not confirmed:
        return {"pending": "needs the customer's confirmation"}
    return tool["function"](**call["arguments"])


cancel = {"name": "cancel_order", "arguments": {"order_id": "ORD-23345"}}
look = {"name": "get_order", "arguments": {"order_id": "ORD-23345"}}
for call, confirmed in [(cancel, False), (cancel, True), (look, False)]:
    print(sorted(dispatch(call, confirmed)))
