`parse_dates(texts)` should turn texts written `day.month.year` into dates
(`format="%d.%m.%Y"`, `errors="coerce"`). Return the number that could not be
read and the ones that could as `YYYY-MM-DD` text: `{"bad": count, "dates":
[...]}`. A day that does not exist, like 31 February, also counts as
unreadable. **Do not write a loop.**

**Expected output:**

```
2
['2026-03-02', '2026-03-15']
```
