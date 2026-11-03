def collection_order(sources):
    ordered = sorted(sources, key=lambda s: (s[1], s[0]))
    return [name for name, volatility in ordered]

SOURCES = [
    ["backup tapes", 5],
    ["memory", 1],
    ["disk", 4],
    ["processes", 2],
    ["connections", 2],
]
for name in collection_order(SOURCES):
    print(name)
