from pathlib import Path


def change_suffix(path, new):
    # Path(path).with_suffix(...)
    return path

print(change_suffix("reports/q1.xlsx", ".csv"))
print(change_suffix("photo.JPG", ".png"))
