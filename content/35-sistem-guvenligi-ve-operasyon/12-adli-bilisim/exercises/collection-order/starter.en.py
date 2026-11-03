def collection_order(sources):
    return [name for name, volatility in sorted(sources)]

SOURCES = [
    ["backup tapes", 5],
    ["memory", 1],
    ["disk", 4],
    ["processes", 2],
    ["connections", 2],
]
for name in collection_order(SOURCES):
    print(name)
