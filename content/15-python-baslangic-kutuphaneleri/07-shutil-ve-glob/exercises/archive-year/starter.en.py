import shutil
from pathlib import Path


def archive_year(folder, year):
    target = Path(folder) / "archive" / str(year)
    # Path(folder).glob(f"{year}-*.txt")
    return []

print(archive_year("logs", 2025))
print(sorted(p.name for p in Path("logs").glob("*.txt")))
