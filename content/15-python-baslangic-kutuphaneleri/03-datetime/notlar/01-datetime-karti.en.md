## Building

| Code | Result |
|---|---|
| `date(2026, 3, 15)` | 15 March 2026 |
| `datetime(2026, 3, 15, 14, 30)` | 15 March 2026 14:30 |
| `date.today()`, `datetime.now()` | now (different on every run) |
| `date.fromisoformat("2026-03-15")` | from ISO text |
| `datetime.strptime(text, format)` | from any format |
| `datetime.combine(day, time)` | day + time |

## Reading and changing

| Code | What it gives |
|---|---|
| `d.year`, `d.month`, `d.day` | the parts |
| `d.weekday()` / `d.isoweekday()` | Monday 0 / Monday 1 |
| `d.replace(day=1)` | a **new** date with one part changed |
| `dt.date()`, `dt.time()` | the day or the time part |
| `d.isoformat()` | `"2026-03-15"` |
| `d.strftime("%d.%m.%Y")` | `"15.03.2026"` |

Date objects are immutable: `replace` returns a new object, the old one stays
the same.

## Durations

| Code | Result |
|---|---|
| `b - a` | a `timedelta` |
| `a + timedelta(days=7)` | one week later |
| `delta.days` | the number of whole days |
| `delta.total_seconds()` | the whole duration in seconds |
| `delta / timedelta(hours=1)` | how many hours the duration is (decimal) |

## Time zones

| Code | What it does |
|---|---|
| `ZoneInfo("Europe/Istanbul")` | a time zone |
| `datetime(..., tzinfo=ZoneInfo(...))` | an aware object |
| `dt.astimezone(ZoneInfo(...))` | shows the same moment on another clock |
| `timezone.utc` | UTC |
| `dt.utcoffset()` | the UTC difference on that date |

## Checklist

- Check the format when reading text: `%m` month, `%M` minute.
- Store in ISO format and, where possible, in UTC.
- Do not mix naive and aware objects.
- Do not write `timedelta(days=30)` for "one month later"; see the second
  note.
