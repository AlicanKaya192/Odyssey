Write the function `format_duration(seconds)`: turn an integer number of
seconds into text in the format `"01:02:05"` (hours:minutes:seconds, two
digits). Use `divmod`: divide by 3600 first, then by 60. Hours can exceed 24
(`90061` → `"25:01:01"`).

**Expected output:**

```
01:02:05
25:01:01
00:00:59
```
