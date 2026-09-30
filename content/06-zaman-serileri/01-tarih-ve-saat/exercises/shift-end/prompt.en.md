The start and length of three night shifts are known:

```python
shifts = [
    ("2024-03-08 22:15", 7, 50),   # start, hours, minutes
    ("2024-03-09 23:40", 6, 30),
    ("2024-03-10 21:05", 9, 0),
]
```

**What to do:**

1. Loop through the list. For each shift read the start with
   `fromisoformat`, build the length with `timedelta(hours=..., minutes=...)`
   and compute the end.
2. For each shift print the end as `"%Y-%m-%d %H:%M"` and the name of the day
   it ends on (`%A`) on one line.
3. Print the total length of the three shifts in **hours** (one decimal).
   Accumulate the total as a `timedelta` and finish with
   `total_seconds() / 3600`.

**Expected output:**

```
2024-03-09 06:05 Saturday
2024-03-10 06:10 Sunday
2024-03-11 06:05 Monday
23.3
```

Every shift that crossed midnight landed on the next day; the date changed
by itself. Code that counts "22 + 7 = 29" by hand would already have gone
wrong here.
