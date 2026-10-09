import shutil
from pathlib import Path


def backup_file(path, folder):
    Path(folder).mkdir(parents=True, exist_ok=True)
    copied = shutil.copy2(path, folder)
    return Path(copied).as_posix()

print(backup_file("notes.txt", "backup"))
print(Path("backup/notes.txt").read_text(encoding="utf-8"))
