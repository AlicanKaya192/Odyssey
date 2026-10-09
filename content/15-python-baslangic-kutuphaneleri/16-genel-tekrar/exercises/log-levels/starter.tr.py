import re
from collections import Counter
from pathlib import Path


def log_levels(path):
    counts = Counter()
    # Path(path).read_text(...).splitlines()
    return dict(counts)

levels = log_levels("app.log")
for level in sorted(levels):
    print(level, levels[level])
