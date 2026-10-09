from contextlib import suppress
from pathlib import Path


def remove_all(paths):
    removed = 0
    for path in paths:
        with suppress(FileNotFoundError):
            Path(path).unlink()
            removed += 1
    return removed

for name in ["a.txt", "b.txt"]:
    Path(name).write_text("x", encoding="utf-8")
print(remove_all(["a.txt", "missing.txt", "b.txt"]))
print(Path("a.txt").exists(), Path("b.txt").exists())
