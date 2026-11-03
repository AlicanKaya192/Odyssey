def overflow_report(writes):
    lines = []
    for name, size, written in sorted(writes):
        if written > size:
            lines.append(f"{name}: {written - size} bytes over")
    if not lines:
        return ["no overflow"]
    return lines

WRITES = [
    ["name", 8, 12],
    ["header", 16, 16],
    ["body", 64, 70],
    ["tag", 4, 3],
]
for line in overflow_report(WRITES):
    print(line)
