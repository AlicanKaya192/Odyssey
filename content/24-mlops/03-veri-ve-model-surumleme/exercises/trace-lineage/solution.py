def trace(records, start):
    chain = []
    name = start
    while name is not None:
        if name not in records:
            chain.append(name + " (missing)")
            break
        chain.append(name)
        name = records[name]["from"]
    return chain


records = {
    "model-3": {"from": "data-v3"},
    "data-v3": {"from": "data-v2"},
    "data-v2": {"from": "data-v1"},
    "data-v1": {"from": None},
    "model-4": {"from": "data-v5"},
}
for name in trace(records, "model-3"):
    print(name)
print("---")
for name in trace(records, "model-4"):
    print(name)
