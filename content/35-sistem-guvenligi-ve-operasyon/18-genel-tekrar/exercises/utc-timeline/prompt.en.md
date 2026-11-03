Each event is `[time, source, text]`; the times are in different time
zones (`Z`, `+00:00`, `+03:00`...). `utc_timeline(events)` should convert
the events to **UTC**, sort them by time and return `"HH:MM:SS source
text"` lines (the time in UTC). Sorting as text misleads. Logging and
Monitoring, Digital Forensics.

**Expected output:**

```
09:00:05 auth reset
09:00:05 fw block
09:00:10 web login
09:00:20 db query
```
