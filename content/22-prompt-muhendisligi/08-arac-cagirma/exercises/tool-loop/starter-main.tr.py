import json

from llm_client import ChatClient
from shop_data import ORDERS

SYSTEM = "You are a shop assistant. Use the tools to look up orders."
SCHEMA = [{"name": "get_order", "description": "Look up an order.",
           "parameters": ["order_id"]}]


def run_tool(call):
    if call["name"] != "get_order":
        return {"error": f"unknown tool {call['name']}"}
    order = ORDERS.get(call["arguments"].get("order_id"))
    if order is None:
        return {"error": "no such order"}
    return {"status": order["status"], "date": order["date"]}


def answer(script, question):
    return ["", [], 0]


SCRIPT = [{"tool_calls": [{"name": "get_order",
                           "arguments": {"order_id": "ORD-23345"}}]},
          "Your order is being prepared."]
text, roles, calls = answer(SCRIPT, "Where is ORD-23345?")
print(text)
print(roles)
print(calls)
