def rollback_target(history):
    # The current version is the last item's version; go through the earlier ones from the end.
    pass


history = [
    ["1.0.0", "ok"],
    ["1.1.0", "ok"],
    ["1.2.0", "failed"],
    ["1.2.1", "ok"],
    ["1.3.0", "failed"],
]
print(rollback_target(history))
print(rollback_target([["2.0.0", "ok"], ["2.0.0", "ok"]]))
print(rollback_target([["0.1.0", "failed"], ["0.2.0", "failed"]]))
print(rollback_target([["1.0.0", "ok"], ["1.1.0", "failed"], ["1.1.0", "failed"]]))
