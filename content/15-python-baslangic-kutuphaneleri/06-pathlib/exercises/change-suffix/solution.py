from pathlib import Path


def change_suffix(path, new):
    return Path(path).with_suffix(new).as_posix()

print(change_suffix("reports/q1.xlsx", ".csv"))
print(change_suffix("photo.JPG", ".png"))
