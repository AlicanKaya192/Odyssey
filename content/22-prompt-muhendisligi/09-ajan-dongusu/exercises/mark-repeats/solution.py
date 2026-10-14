import json


def mark_repeats(calls):
    seen, marks = set(), []
    for call in calls:
        key = json.dumps(call, sort_keys=True)
        marks.append("repeat" if key in seen else "run")
        seen.add(key)
    return marks


A = {"name": "get_order", "arguments": {"order_id": "ORD-1"}}
B = {"arguments": {"order_id": "ORD-1"}, "name": "get_order"}
C = {"name": "get_order", "arguments": {"order_id": "ORD-2"}}
print(mark_repeats([A, C, B, C]))
