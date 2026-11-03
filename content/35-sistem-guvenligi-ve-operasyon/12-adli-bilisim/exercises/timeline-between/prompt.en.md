Each record is `[path, kind, time]`; the time is `"HH:MM:SS"` text.
`timeline_between(records, start, end)` should return the records whose
time is between `start` and `end` (both **inclusive**) as `"<time> <kind>
<path>"` lines, sorted by time and then path. Time texts in the same format
can be compared directly.

**Expected output:**

```
02:19:58 accessed /srv/data/customers.csv
02:20:03 modified /tmp/x.zip
```
