`sources` is source name → list of `[timestamp, text]`; timestamps are ISO
text with a time zone. `build_timeline(sources)` should convert every
event to UTC and return them in time order as `"<HH:MM:SS> <source>
<text>"` lines (time format `strftime("%H:%M:%S")`, in UTC). Events at the
same moment are ordered by source name.

**Expected output:**

```
02:14:00 vpn login bob
02:15:10 db new db user
02:16:30 web admin page
02:20:05 db table exported
```
