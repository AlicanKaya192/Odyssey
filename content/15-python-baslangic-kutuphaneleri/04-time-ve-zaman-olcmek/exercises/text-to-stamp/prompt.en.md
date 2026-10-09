Write the function `text_to_stamp(text)`: turn a **UTC** time in the format
`"2026-03-15 14:30"` into a timestamp and return it as an **integer**.
Steps: `strptime`, `replace(tzinfo=timezone.utc)`, `timestamp()`, `int`.

**Expected output:**

```
1773585000
86400
```
