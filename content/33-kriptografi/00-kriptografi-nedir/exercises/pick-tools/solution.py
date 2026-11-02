def pick_tools(needs):
    tools = []
    if needs.get("secret"):
        tools.append("encryption")
    if needs.get("password"):
        tools.append("password-hash")
    if needs.get("third_party"):
        tools.append("signature")
    elif needs.get("tamper"):
        tools.append("mac")
    return sorted(tools)

print(pick_tools({"secret": True}))
print(pick_tools({"tamper": True}))
print(pick_tools({"tamper": True, "third_party": True}))
print(pick_tools({"secret": True, "password": True}))
print(pick_tools({}))
