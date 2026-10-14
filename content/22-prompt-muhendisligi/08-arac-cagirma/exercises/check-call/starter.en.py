import re


def check_call(call, specs):
    return "ok"


SPECS = {"get_order": {"order_id": r"ORD-\d{5}"}}
for call in [{"name": "get_order", "arguments": {"order_id": "ORD-48213"}},
             {"name": "get_order", "arguments": {"id": "ORD-48213"}},
             {"name": "get_order", "arguments": {"order_id": "ORD-1"}},
             {"name": "refund", "arguments": {}}]:
    print(check_call(call, SPECS))
