Write the function `parse_date(text)`: find the **first** date in the
format `dd.mm.yyyy` in the text and return the tuple `(year, month, day)` as
**integers**; if there is no date, `None`. Use three groups:
`(\d{2})\.(\d{2})\.(\d{4})`.

**Expected output:**

```
(2026, 3, 15)
None
```
