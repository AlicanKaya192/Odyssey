from pathlib import Path


def fits(folder, free):
    total = 0
    # her dosyanin stat().st_size degerini topla
    return total, total <= free

print(fits("media", 100))
print(fits("media", 10))
