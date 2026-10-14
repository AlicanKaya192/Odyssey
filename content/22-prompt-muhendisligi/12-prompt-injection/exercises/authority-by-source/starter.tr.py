def allowed(tool, source, tools):
    return True


TOOLS = {"get_order": {"irreversible": False},
         "cancel_order": {"irreversible": True}}
for tool, source in [("get_order", "document"), ("cancel_order", "document"),
                     ("cancel_order", "user"), ("refund", "user")]:
    print(tool, source, allowed(tool, source, TOOLS))
