import bisect
import math


def drift_report(reference, current, columns, bins):
    report = []
    for name in columns:
        ordered = sorted(r[name] for r in reference)
        edges = [ordered[len(ordered) * i // bins] for i in range(1, bins)]

        def shares(rows):
            counts = [0] * bins
            for r in rows:
                counts[bisect.bisect_left(edges, r[name])] += 1
            return [max(c / len(rows), 0.0001) for c in counts]

        ref, cur = shares(reference), shares(current)
        value = sum((c - r) * math.log(c / r) for r, c in zip(ref, cur))
        if value < 0.1:
            label = "stable"
        elif value <= 0.25:
            label = "moderate"
        else:
            label = "large"
        report.append([name, round(value, 3), label])
    return report


reference = [{"fee": f, "calls": c} for f, c in zip(range(20, 40), [0, 1] * 10)]
current = [{"fee": f + 8, "calls": c} for f, c in zip(range(20, 40), [0, 1] * 10)]
for row in drift_report(reference, current, ["fee", "calls"], 4):
    print(row)
