from pathlib import Path


def organize(folder):
    base = Path(folder)
    for path in list(base.iterdir()):
        if not path.is_file():
            continue
        kind = path.suffix.lower().lstrip(".") or "other"
        (base / kind).mkdir(exist_ok=True)
        path.rename(base / kind / path.name)
    files = [p for p in base.rglob("*") if p.is_file()]
    return sorted(p.relative_to(base).as_posix() for p in files)

for path in organize("inbox"):
    print(path)
