def schema(tools):
    return [{"name": name, "description": tool["description"],
             "parameters": list(tool["parameters"])}
            for name, tool in tools.items()]


TOOLS = {
    "get_order": {"description": "Look up an order.",
                  "parameters": {"order_id": r"ORD-\d{5}"}},
    "order_total": {"description": "Total of an order.",
                    "parameters": {"order_id": r"ORD-\d{5}",
                                   "currency": r"[A-Z]{3}"}},
}
for item in schema(TOOLS):
    print(item["name"], item["parameters"])
