from shop_data import ORDERS


def get_order(order_id):
    order = ORDERS[order_id]
    return {"status": order["status"]}


TOOLS = {"get_order": get_order}


def run_tool(call):
    return TOOLS[call["name"]](**call["arguments"])


for call in [{"name": "get_order", "arguments": {"order_id": "ORD-48213"}},
             {"name": "get_order", "arguments": {"order_id": "ORD-00000"}},
             {"name": "get_order", "arguments": {"id": "ORD-48213"}},
             {"name": "refund"}]:
    print(run_tool(call))
