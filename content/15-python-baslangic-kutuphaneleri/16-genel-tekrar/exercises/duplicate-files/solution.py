from collections import defaultdict
from pathlib import Path


def duplicate_files(folder):
    base = Path(folder)
    groups = defaultdict(list)
    for path in base.rglob("*"):
        if path.is_file():
            content = path.read_text(encoding="utf-8")
            groups[content].append(path.relative_to(base).as_posix())
    return sorted(sorted(paths) for paths in groups.values() if len(paths) > 1)

for group in duplicate_files("files"):
    print(group)
