def rollback_target(history):
    # Su anki surum son ogenin surumu; ondan oncekileri sondan basa gez.
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
