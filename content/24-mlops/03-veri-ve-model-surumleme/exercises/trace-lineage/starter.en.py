def trace(records, start):
    # Climb up with "from" until the name is None.
    pass


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
