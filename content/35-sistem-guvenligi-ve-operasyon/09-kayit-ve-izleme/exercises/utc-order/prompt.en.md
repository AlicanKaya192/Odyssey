Each event is `[timestamp, text]`; timestamps are ISO text with a time
zone (`"2026-11-01T10:00:05+03:00"`). `utc_order(events)` should return
the event texts in **real** time order: read the timestamps with
`datetime.fromisoformat` and compare them. Sorting the timestamps as text
gives the wrong result.

**Expected output:**

```
file deleted
login from new place
admin group changed
```
