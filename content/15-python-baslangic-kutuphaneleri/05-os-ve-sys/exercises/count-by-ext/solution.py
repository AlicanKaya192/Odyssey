import os


def count_by_ext(folder):
    counts = {}
    for root, dirs, files in os.walk(folder):
        for name in files:
            ext = os.path.splitext(name)[1]
            counts[ext] = counts.get(ext, 0) + 1
    return counts

counts = count_by_ext("project")
for ext in sorted(counts):
    print(repr(ext), counts[ext])
