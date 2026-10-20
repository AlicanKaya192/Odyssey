def previous_version(history, alias):
    # Collect the alias's versions, find the different one going backwards from the end.
    pass


history = [
    ["production", 1],
    ["staging", 2],
    ["production", 3],
    ["staging", 4],
]
print(previous_version(history, "production"))
print(previous_version(history, "staging"))
print(previous_version([["production", 1]], "production"))
