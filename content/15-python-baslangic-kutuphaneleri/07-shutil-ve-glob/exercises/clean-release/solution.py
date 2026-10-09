import shutil
from pathlib import Path


def clean_release(src, dst):
    skip = shutil.ignore_patterns("*.tmp", "temp")
    shutil.copytree(src, dst, ignore=skip, dirs_exist_ok=True)
    files = [p for p in Path(dst).rglob("*") if p.is_file()]
    return sorted(p.relative_to(dst).as_posix() for p in files)

for name in clean_release("app", "release"):
    print(name)
