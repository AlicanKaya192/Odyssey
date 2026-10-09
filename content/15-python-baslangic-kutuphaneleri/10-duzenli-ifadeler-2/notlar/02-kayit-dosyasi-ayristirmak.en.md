One of the most common uses of regex is parsing a **log file**: splitting
every line into date, time, level, part and message, then counting and
filtering. The way to keep a long pattern readable is the **`re.VERBOSE`**
flag and named groups.

```python
import re

LOG = """2026-03-15 10:02:11 ERROR [db] connection lost
2026-03-15 10:02:15 INFO [web] request /home 200
2026-03-15 10:03:40 WARNING [db] slow query 2.4s
bad line without format
2026-03-15 10:05:02 ERROR [web] request /cart 500
2026-03-15 10:06:30 ERROR [db] connection lost"""

LINE = re.compile(r"""
    (?P<date>\d{4}-\d{2}-\d{2})\s
    (?P<time>\d{2}:\d{2}:\d{2})\s
    (?P<level>[A-Z]+)\s
    \[(?P<part>\w+)\]\s
    (?P<message>.+)
""", re.VERBOSE)

counts = {}
skipped = []
for line in LOG.splitlines():
    m = LINE.fullmatch(line)
    if m is None:
        skipped.append(line)
        continue
    key = (m["level"], m["part"])
    counts[key] = counts.get(key, 0) + 1
for key in sorted(counts):
    print(key, counts[key])
print("skipped:", skipped)
```

```text
('ERROR', 'db') 2
('ERROR', 'web') 1
('INFO', 'web') 1
('WARNING', 'db') 1
skipped: ['bad line without format']
```

## What happens?

- **`re.VERBOSE`**: spaces and line breaks in the pattern are ignored
  (comments with `#` can be written too). We could put each piece on its own
  line. The price: to search for a real space, write **`\s`** (or `\ `).
- **Named groups** make the pattern explain itself; `m["level"]` is short
  for `m.group("level")`.
- `\[` and `\]`: the square brackets themselves; without the backslash they
  would be taken for a character class.
- **`fullmatch`**: the whole line must fit the format. The line that did not
  fit was not silently skipped; it went into the **`skipped`** list. Real log
  files always have off-format lines; knowing how many there are shows
  whether the pattern misses something.
- The counter key is the `(level, part)` tuple: the database part had two
  `ERROR`s.

`collections.Counter` in the next section makes the counting shorter.
