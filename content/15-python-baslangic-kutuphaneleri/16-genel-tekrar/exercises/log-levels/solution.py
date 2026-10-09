import re
from collections import Counter
from pathlib import Path

LINE = re.compile(r"\S+ \S+ (\w+) \[\w+\] .+")


def log_levels(path):
    counts = Counter()
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = LINE.fullmatch(line)
        if m:
            counts[m.group(1)] += 1
    return dict(counts)

levels = log_levels("app.log")
for level in sorted(levels):
    print(level, levels[level])
