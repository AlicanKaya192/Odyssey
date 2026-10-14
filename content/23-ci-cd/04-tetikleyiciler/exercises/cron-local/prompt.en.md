Write the function `turkey_time(cron)`. It should return the **Turkey time** of a cron expression as `"HH:MM"`:

- The first field is the minute, the second the hour (UTC).
- Turkey time = UTC + 3; past 24 it wraps around (`22` → `01`).
- The hour and minute have two digits: `"06:00"`, `"06:17"`.
- If the hour field is `*`: `"every hour at minute "` + the minute field.

**Expected output:**

```
06:00
06:17
01:30
every hour at minute 5
```
