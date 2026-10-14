import json

from llm_client import ChatClient
from shop_data import ORDERS

SYSTEM = "You are a shop assistant. Use the tools; answer when you know."
SCHEMA = [{"name": "get_order", "parameters": ["order_id"]}]


def run_tool(call):
    if call["name"] != "get_order":
        return {"error": f"unknown tool {call['name']}"}
    order = ORDERS.get(call.get("arguments", {}).get("order_id"))
    if order is None:
        return {"error": "no such order"}
    return {"status": order["status"]}


def agent(script, question, max_steps):
    return [None, 0, []]


LOOK = {"tool_calls": [{"name": "get_order",
                        "arguments": {"order_id": "ORD-23345"}}]}
for script in [[LOOK, "It is being prepared."], [LOOK] * 4]:
    text, steps, trace = agent(script, "Where is ORD-23345?", 3)
    print(text, steps)
    print(trace)
