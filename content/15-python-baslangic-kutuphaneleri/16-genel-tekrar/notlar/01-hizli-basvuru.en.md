## Imports

```python
import math, statistics, random
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import time, os, sys, shutil, glob, csv, re
from pathlib import Path
from collections import Counter, defaultdict, deque, namedtuple
from itertools import chain, groupby, islice, pairwise, batched, accumulate
import string, textwrap, difflib, unicodedata
import zipfile, gzip, tempfile, copy
from pprint import pprint
from enum import Enum
```

## The most used one-liners

| Job | Code |
|---|---|
| Are the decimals equal | `math.isclose(a, b)` |
| A reproducible die | `random.Random(7).randint(1, 6)` |
| Today's ISO date | `date.today().isoformat()` |
| A date from text | `datetime.strptime(s, "%d.%m.%Y")` |
| Days between two dates | `(b - a).days` |
| Measuring a duration | `t = time.perf_counter(); ...; time.perf_counter() - t` |
| Data next to the file | `Path(__file__).parent / "data.csv"` |
| All CSVs | `sorted(Path("data").rglob("*.csv"))` |
| Reading a file | `Path(p).read_text(encoding="utf-8")` |
| Copying a folder | `shutil.copytree(a, b, dirs_exist_ok=True)` |
| CSV rows as dictionaries | `list(csv.DictReader(open(p, newline="", encoding="utf-8")))` |
| All numbers | `re.findall(r"-?\d+", s)` |
| Is the format right | `re.fullmatch(r"[A-Z]{2}-\d{4}", s)` |
| The 5 most frequent | `Counter(items).most_common(5)` |
| Grouping | `g = defaultdict(list); g[k].append(v)` |
| Consecutive differences | `[b - a for a, b in pairwise(xs)]` |
| Wrapping into lines | `textwrap.wrap(s, 60)` |
| Did you mean | `difflib.get_close_matches(w, options, n=1)` |
| Zipping a folder | `shutil.make_archive("name", "zip", root_dir=d)` |
| A temporary folder | `with tempfile.TemporaryDirectory() as tmp:` |
| An independent copy | `copy.deepcopy(x)` |

## Format codes

| Code | Meaning |
|---|---|
| `%Y-%m-%d` | 2026-03-15 |
| `%d.%m.%Y` | 15.03.2026 |
| `%H:%M:%S` | 14:30:00 |
| `%A`, `%B` | day name, month name (language-dependent) |

## Regex

`\d` digit, `\w` word character, `\s` whitespace, `.` anything; `?` `*` `+`
`{n,m}`; `^ $ \b`; `( )` group, `(?P<name> )` named group, `(?: )`
non-capturing; `+?` lazy; flags `re.I`, `re.M`, `re.X`.
