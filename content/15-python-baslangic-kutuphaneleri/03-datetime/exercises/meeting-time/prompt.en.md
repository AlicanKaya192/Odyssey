Write the function `meeting_time(local, from_zone, to_zone)`: `local` is a
moment in the format `"2026-03-15 14:30"` in the time zone `from_zone`. Show
it in the time zone `to_zone` and return only the time in the format
`"07:30"`. Steps: `strptime`, `replace(tzinfo=ZoneInfo(from_zone))`,
`astimezone(ZoneInfo(to_zone))`, `strftime("%H:%M")`.

**Expected output:**

```
07:30
17:00
```
