from pathlib import Path


def fits(folder, free):
    total = 0
    for path in Path(folder).rglob("*"):
        if path.is_file():
            total += path.stat().st_size
    return total, total <= free

print(fits("media", 100))
print(fits("media", 10))
