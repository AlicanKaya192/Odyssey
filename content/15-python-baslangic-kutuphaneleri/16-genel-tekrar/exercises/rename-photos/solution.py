import re
from datetime import datetime
from pathlib import Path

PHOTO = re.compile(r"IMG_(\d{8}_\d{6})\.jpg")


def rename_photos(folder):
    base = Path(folder)
    for path in list(base.iterdir()):
        m = PHOTO.fullmatch(path.name)
        if m:
            taken = datetime.strptime(m.group(1), "%Y%m%d_%H%M%S")
            path.rename(base / taken.strftime("%Y-%m-%d_%H-%M-%S.jpg"))
    return sorted(p.name for p in base.iterdir())

for name in rename_photos("photos"):
    print(name)
