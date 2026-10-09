import shutil
from pathlib import Path


def archive_year(folder, year):
    target = Path(folder) / "archive" / str(year)
    target.mkdir(parents=True, exist_ok=True)
    for path in Path(folder).glob(f"{year}-*.txt"):
        shutil.move(path, target)
    return sorted(p.name for p in target.iterdir())

print(archive_year("logs", 2025))
print(sorted(p.name for p in Path("logs").glob("*.txt")))
