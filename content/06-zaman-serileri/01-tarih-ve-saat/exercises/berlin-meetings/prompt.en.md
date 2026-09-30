The team in Berlin meets every day at 09:00; the team in Istanbul
joins in. On the night of 31 March 2024 Berlin moved its clocks one hour
forward.

**What to do:**

1. Define `berlin = ZoneInfo("Europe/Berlin")` and
   `istanbul = ZoneInfo("Europe/Istanbul")`.
2. Build the Berlin meetings on 30 March 2024 09:00 and 31 March 2024 09:00
   as aware `datetime` objects (`tzinfo=berlin`).
3. Find their Istanbul times with `astimezone(istanbul)` and print them as
   `"%H:%M"`, one per line.
4. Compute how many hours **really** passed in Berlin between 30 March 12:00
   and 31 March 12:00: convert both to UTC with `astimezone(timezone.utc)`
   and print the difference's `total_seconds() / 3600`.

**Expected output:**

```
11:00
10:00
23.0
```

Seen from Istanbul, the meeting moved one hour earlier overnight. The last
line tells the truth that subtracting in the same zone hides: that "one day"
lasted 23 hours.
