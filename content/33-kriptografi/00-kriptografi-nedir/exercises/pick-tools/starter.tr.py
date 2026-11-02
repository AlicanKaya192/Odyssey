def pick_tools(needs):
    tools = []
    if needs["secret"]:
        tools.append("base64")
    return tools

print(pick_tools({"secret": True}))
print(pick_tools({"tamper": True}))
print(pick_tools({"tamper": True, "third_party": True}))
print(pick_tools({"secret": True, "password": True}))
print(pick_tools({}))
