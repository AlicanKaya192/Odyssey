import re
from datetime import datetime
from pathlib import Path


def rename_photos(folder):
    base = Path(folder)
    # re.fullmatch, strptime, strftime, rename
    return sorted(p.name for p in base.iterdir())

for name in rename_photos("photos"):
    print(name)
