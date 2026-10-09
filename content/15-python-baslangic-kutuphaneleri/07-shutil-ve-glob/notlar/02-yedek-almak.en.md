A small tool that combines what you learned in this section: a function that
takes a **dated backup** of a project folder and keeps only the last few
backups.

```python
import shutil
from datetime import datetime
from pathlib import Path

for name in ["project/main.py", "project/data/sales.csv", "project/debug.log"]:
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")


def backup(source, root, now, keep=3):
    name = Path(source).name
    target = Path(root) / f"{name}-{now:%Y%m%d-%H%M}"
    shutil.copytree(source, target, ignore=shutil.ignore_patterns("*.log"))
    backups = sorted(Path(root).glob(f"{name}-*"))
    for old in backups[:-keep]:
        shutil.rmtree(old)
    return [b.name for b in sorted(Path(root).iterdir())]


for hour in [9, 12, 15, 18]:
    print(backup("project", "backups", datetime(2026, 3, 15, hour, 0)))
```

```text
['project-20260315-0900']
['project-20260315-0900', 'project-20260315-1200']
['project-20260315-0900', 'project-20260315-1200', 'project-20260315-1500']
['project-20260315-1200', 'project-20260315-1500', 'project-20260315-1800']
```

What happens:

- **The folder name comes from the date:** `f"{now:%Y%m%d-%H%M}"` uses a
  `strftime` format inside the f-string. The year-month-day-hour order makes
  **sorting the names as text the same as sorting by date**; `sorted` puts the
  oldest first.
- **Log files are skipped:** `ignore_patterns("*.log")`.
- **The last 3 backups:** `backups[:-keep]` is everything except the last
  `keep`; those are deleted with `rmtree`. With the fourth backup, the 09:00
  backup went away.
- **The time comes in as a parameter:** the function does not call
  `datetime.now()` itself. So the same input gives the same result and it can
  be tested; in real use you write `backup("project", "backups",
  datetime.now())`.

A real backup tool has one more step: backups are taken to **another disk**
(an external disk, a network folder). A backup on the same disk goes with the
project when the disk fails.
