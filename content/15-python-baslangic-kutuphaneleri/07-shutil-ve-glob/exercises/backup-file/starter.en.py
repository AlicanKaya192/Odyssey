import shutil
from pathlib import Path


def backup_file(path, folder):
    return shutil.copy2(path, folder)

print(backup_file("notes.txt", "backup"))
print(Path("backup/notes.txt").read_text(encoding="utf-8"))
