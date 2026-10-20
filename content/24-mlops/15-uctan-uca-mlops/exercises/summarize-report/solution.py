def summarize(lines):
    counts = {"keep": 0, "promoted": 0, "kept out": 0, "data rejected": 0}
    for line in lines:
        decision = line.split("->")[1]
        for kind in counts:
            if kind in decision:
                counts[kind] += 1
                break
    return [counts["keep"], counts["promoted"], counts["kept out"], counts["data rejected"]]


report = [
    "month 1: drift 0.070 acc 0.813 -> keep",
    "month 3: drift 0.578 acc 0.778 -> v2 promoted (0.782)",
    "month 4: drift 0.326 acc 0.787 -> candidate kept out (0.784)",
    "month 5: drift 0.575 acc 0.691 -> data rejected (100% invalid)",
    "month 7: drift 0.127 acc 0.821 -> keep",
]
print(summarize(report))
print(summarize([]))
