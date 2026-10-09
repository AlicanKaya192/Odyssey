# Overall Review

You have reached the end of the Python Libraries: Beginner module. In a
script you can now do most jobs involving numbers, dates, files, folders,
CSV, text and patterns with the standard library alone, installing no
package. This section walks the path once more; at the end there is an
example where the module's tools work together.

<figure class="fig">
  <div class="flow">
    <span class="node">Numbers<br><small>01–02</small></span><span class="arrow">→</span>
    <span class="node">Time<br><small>03–04</small></span><span class="arrow">→</span>
    <span class="node">Files<br><small>05–08, 14</small></span><span class="arrow">→</span>
    <span class="node">Text<br><small>09–10, 13</small></span><span class="arrow">→</span>
    <span class="node acc">Structures<br><small>11–12, 15</small></span>
  </div>
  <figcaption>The module's path: numbers and time, then files and text, and data structures at the end.</figcaption>
</figure>

## 1. The standard library (Section 0)

About 300 modules come with Python (`sys.stdlib_module_names`); no
installation is needed and they are the same on every computer. `dir(module)`
and `help(...)` tell what a module offers. Before looking for a package for a
job, look in the standard library.

## 2. Numbers: math, statistics, random (Sections 1–2)

| Job | Tool |
|---|---|
| Comparing decimals | `math.isclose(a, b)` |
| Rounding up / down | `math.ceil`, `math.floor` |
| Combinations, permutations | `math.comb`, `math.perm` |
| Mean, median, standard deviation | `statistics.mean`, `median`, `stdev` |
| Probability in a normal distribution | `statistics.NormalDist(...).cdf(x)` |
| Reproducible randomness | `random.Random(seed)` |
| Picking | `choice`, `choices(..., weights=)`, `sample` |

`0.1 + 0.2 == 0.3` is false; `round(2.5)` is 2 (banker's rounding); the same
seed gives the same sequence.

## 3. Time: datetime, time (Sections 3–4)

| Job | Tool |
|---|---|
| Building a date | `date(2026, 3, 15)`, `datetime(...)` |
| Differences, adding | `timedelta`; the whole duration `total_seconds()` |
| Text ↔ date | `strftime` / `strptime`; `isoformat` for ISO |
| Time zones | `ZoneInfo("Europe/Istanbul")`, `astimezone` |
| Measuring durations | the difference of `time.perf_counter()` |
| Waiting | `time.sleep(seconds)` |

`%m` is the month, `%M` the minute; `timedelta` has no months; measure
durations with `perf_counter`, not `time.time()`.

## 4. The file system (Sections 5–7)

| Job | Tool |
|---|---|
| Building paths, parts | `Path("a") / "b"`, `.name`, `.stem`, `.suffix`, `.parent` |
| Reading, writing | `read_text` / `write_text` (`encoding="utf-8"`) |
| Creating folders | `mkdir(parents=True, exist_ok=True)` |
| Searching | `glob("*.csv")`, `rglob("*.csv")` |
| Walking a tree | `os.walk` |
| Copying, moving | `shutil.copy2`, `copytree`, `move` |
| Deleting a full folder | `shutil.rmtree` (permanent!) |
| Environment variables | `os.environ.get(name, default)` |
| Version, arguments | `sys.version_info`, `sys.argv` |

## 5. Data files (Sections 8 and 14)

- CSV: `open(..., newline="", encoding="utf-8")`, `DictReader` /
  `DictWriter`; values are text; for Excel `utf-8-sig` and `;`.
- Archives: `zipfile.ZipFile(..., compression=ZIP_DEFLATED)`,
  `shutil.make_archive`, `gzip.open(..., "rt")`.
- Temporary: `tempfile.TemporaryDirectory()`; safe writing is a temporary
  file + `os.replace`.

## 6. Text (Sections 9–10 and 13)

| Job | Tool |
|---|---|
| Searching for a pattern | `re.search`, `re.findall`; validating `re.fullmatch` |
| Pulling out parts | groups `(...)`, named `(?P<name>...)` |
| Replacing, splitting | `re.sub` (`\1` or a function), `re.split` |
| Wrapping into lines | `textwrap.wrap`, `shorten`, `dedent` |
| Similarity, differences | `difflib.get_close_matches`, `unified_diff` |
| Dropping accents | `unicodedata.normalize("NFD", ...)` + `Mn` |

Patterns are `r"..."`; a regex checks the form, check the meaning in Python;
do not trust `lower()` for the Turkish `I`/`İ`.

## 7. Data structures (Sections 11–12 and 15)

| Job | Tool |
|---|---|
| Counting | `Counter(...).most_common(n)` |
| Grouping | `defaultdict(list)` |
| A named record | `namedtuple` |
| A queue, the last N | `deque`, `deque(maxlen=N)` |
| Consecutive, pieces, running | `pairwise`, `batched`, `accumulate` |
| Combinations | `product`, `permutations`, `combinations` |
| An independent copy | `copy.deepcopy` |
| Readable printing | `pprint(..., depth=)` |
| Fixed options | `Enum`, `IntEnum`, `Flag` |

## All together

A small tool that pulls the errors out of a log file, counts them by day and
writes the most frequent errors to a CSV report: `pathlib`, `re`,
`datetime`, `collections` and `csv` together.

```python
import csv
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

log = Path("app.log")
log.write_text(
    "2026-03-15 10:02:11 ERROR [db] connection lost\n"
    "2026-03-15 10:02:15 INFO [web] request ok\n"
    "2026-03-15 11:40:03 ERROR [web] timeout\n"
    "2026-03-16 09:05:44 ERROR [db] connection lost\n",
    encoding="utf-8",
)
LINE = re.compile(r"(\S+ \S+) (\w+) \[(\w+)\] (.+)")
errors = Counter()
by_day = Counter()
for line in log.read_text(encoding="utf-8").splitlines():
    m = LINE.fullmatch(line)
    if m and m[2] == "ERROR":
        when = datetime.strptime(m[1], "%Y-%m-%d %H:%M:%S")
        errors[m[4]] += 1
        by_day[when.date().isoformat()] += 1
with open("report.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["message", "count"])
    writer.writerows(errors.most_common())
print(dict(by_day))
print(Path("report.csv").read_text(encoding="utf-8"))
```

```text
{'2026-03-15': 2, '2026-03-16': 1}
message,count
connection lost,2
timeout,1
```

Every line comes from a section: the file is written and read with
`pathlib`, the line is split with `re`, the time is parsed with `datetime`,
the counting is done with `Counter`, the report is written with `csv`. No
package was installed.

## Common mistakes

| Mistake | The right way |
|---|---|
| `0.1 + 0.2 == 0.3` | `math.isclose` |
| `random.seed` everywhere | `random.Random(seed)` |
| `strptime(..., "%H:%m")` | `%M` is the minute |
| Measuring durations with `time.time()` | `perf_counter` |
| Gluing paths with `+` | `Path / "name"` |
| Leaving out `encoding` | `encoding="utf-8"` |
| Reading CSV with `split(",")` | the `csv` module |
| Forgetting `newline=""` | blank lines on Windows |
| Writing a pattern without `r` | `r"\b..."` |
| Not sorting before `groupby` | `sorted(..., key=)` |
| `[[0] * 3] * 3` | a comprehension |
| `"İ".lower()` | convert `I`/`İ` first |
