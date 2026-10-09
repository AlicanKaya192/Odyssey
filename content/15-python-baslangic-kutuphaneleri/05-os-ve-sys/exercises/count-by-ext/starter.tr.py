import os


def count_by_ext(folder):
    counts = {}
    # for root, dirs, files in os.walk(folder):
    return counts

counts = count_by_ext("project")
for ext in sorted(counts):
    print(repr(ext), counts[ext])
