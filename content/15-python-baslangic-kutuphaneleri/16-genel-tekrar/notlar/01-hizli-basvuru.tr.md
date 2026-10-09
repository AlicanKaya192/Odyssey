## İçe aktarmalar

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

## En sık kullanılan tek satırlar

| İş | Kod |
|---|---|
| Ondalık eşit mi | `math.isclose(a, b)` |
| Tekrarlanabilir zar | `random.Random(7).randint(1, 6)` |
| Bugünün ISO tarihi | `date.today().isoformat()` |
| Metinden tarih | `datetime.strptime(s, "%d.%m.%Y")` |
| İki tarih arası gün | `(b - a).days` |
| Süre ölçmek | `t = time.perf_counter(); ...; time.perf_counter() - t` |
| Dosyanın yanındaki veri | `Path(__file__).parent / "data.csv"` |
| Bütün CSV'ler | `sorted(Path("data").rglob("*.csv"))` |
| Dosyayı okumak | `Path(p).read_text(encoding="utf-8")` |
| Klasörü kopyalamak | `shutil.copytree(a, b, dirs_exist_ok=True)` |
| CSV satırları sözlük | `list(csv.DictReader(open(p, newline="", encoding="utf-8")))` |
| Bütün sayılar | `re.findall(r"-?\d+", s)` |
| Biçim doğru mu | `re.fullmatch(r"[A-Z]{2}-\d{4}", s)` |
| En sık 5 | `Counter(items).most_common(5)` |
| Gruplamak | `g = defaultdict(list); g[k].append(v)` |
| Ardışık farklar | `[b - a for a, b in pairwise(xs)]` |
| Satırlara sarmak | `textwrap.wrap(s, 60)` |
| Bunu mu demek istediniz | `difflib.get_close_matches(w, options, n=1)` |
| Klasörü zip'lemek | `shutil.make_archive("ad", "zip", root_dir=k)` |
| Geçici klasör | `with tempfile.TemporaryDirectory() as tmp:` |
| Bağımsız kopya | `copy.deepcopy(x)` |

## Biçim kodları

| Kod | Anlamı |
|---|---|
| `%Y-%m-%d` | 2026-03-15 |
| `%d.%m.%Y` | 15.03.2026 |
| `%H:%M:%S` | 14:30:00 |
| `%A`, `%B` | gün adı, ay adı (dile bağlı) |

## Regex

`\d` rakam, `\w` kelime karakteri, `\s` boşluk, `.` herhangi; `?` `*` `+`
`{n,m}`; `^ $ \b`; `( )` grup, `(?P<ad> )` adlı grup, `(?: )` yakalamayan;
`+?` tembel; bayraklar `re.I`, `re.M`, `re.X`.
