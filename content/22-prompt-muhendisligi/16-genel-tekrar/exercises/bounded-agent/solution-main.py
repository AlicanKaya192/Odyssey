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
    client = ChatClient(script)
    messages = [{"role": "user", "content": question}]
    for round_number in range(1, max_rounds + 1):
        reply = client.chat(messages, tools=TOOLS)
        if not reply.tool_calls:
            return [reply.text, round_number]
        messages.append({"role": "assistant", "content": "",
                         "tool_calls": reply.tool_calls})
        for call in reply.tool_calls:
            if call["name"] == "get_order":
                result = get_order(**call["arguments"])
            else:
                result = {"error": "unknown tool"}
            messages.append({"role": "tool", "content": json.dumps(result)})
    return [None, max_rounds]


CALL = {"tool_calls": [{"name": "get_order",
                        "arguments": {"order_id": "ORD-48213"}}]}
print(run_agent([CALL, "It shipped on 2026-10-09."], "Where?", 3))
print(run_agent([CALL, CALL, CALL], "Where?", 3))
