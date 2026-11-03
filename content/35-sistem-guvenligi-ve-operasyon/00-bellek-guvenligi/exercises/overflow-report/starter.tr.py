def overflow_report(writes):
    lines = []
    for name, size, written in writes:
        # yazilan alani asiyor mu?
        pass
    return lines

WRITES = [
    ["name", 8, 12],
    ["header", 16, 16],
    ["body", 64, 70],
    ["tag", 4, 3],
]
for line in overflow_report(WRITES):
    print(line)
