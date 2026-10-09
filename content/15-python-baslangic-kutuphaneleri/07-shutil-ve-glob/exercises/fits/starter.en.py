from pathlib import Path


def fits(folder, free):
    total = 0
    # add up stat().st_size of every file
    return total, total <= free

print(fits("media", 100))
print(fits("media", 10))
