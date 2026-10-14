import json

from llm_client import ChatClient
from shop_data import ORDERS

TOOLS = [{"name": "get_order", "description": "Look up an order.",
          "parameters": ["order_id"]}]


def get_order(order_id):
    order = ORDERS.get(order_id)
    if order is None:
        return {"error": f"no order {order_id}"}
    return {"status": order["status"], "date": order["date"]}


def run_agent(script, question, max_rounds):
    return [None, 0]


CALL = {"tool_calls": [{"name": "get_order",
                        "arguments": {"order_id": "ORD-48213"}}]}
print(run_agent([CALL, "It shipped on 2026-10-09."], "Where?", 3))
print(run_agent([CALL, CALL, CALL], "Where?", 3))
