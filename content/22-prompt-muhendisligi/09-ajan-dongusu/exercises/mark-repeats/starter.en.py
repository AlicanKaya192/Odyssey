import json


def mark_repeats(calls):
    return []


A = {"name": "get_order", "arguments": {"order_id": "ORD-1"}}
B = {"arguments": {"order_id": "ORD-1"}, "name": "get_order"}
C = {"name": "get_order", "arguments": {"order_id": "ORD-2"}}
print(mark_repeats([A, C, B, C]))
