import re


def check_call(call, specs):
    params = specs.get(call["name"])
    if params is None:
        return f"unknown tool {call['name']}"
    args = call.get("arguments", {})
    if set(args) != set(params):
        return "arguments must be " + ", ".join(params)
    for name, pattern in params.items():
        if not re.fullmatch(pattern, str(args[name])):
            return f"{name} has the wrong form"
    return "ok"


SPECS = {"get_order": {"order_id": r"ORD-\d{5}"}}
for call in [{"name": "get_order", "arguments": {"order_id": "ORD-48213"}},
             {"name": "get_order", "arguments": {"id": "ORD-48213"}},
             {"name": "get_order", "arguments": {"order_id": "ORD-1"}},
             {"name": "refund", "arguments": {}}]:
    print(check_call(call, SPECS))
