Write the function `parse_cve(text)`. If the text is a valid CVE
identifier, return the tuple `(year, number)` (both `int`), otherwise
`None`.

- First remove the spaces at both ends and turn it upper case (`strip`,
  `upper`).
- Split by `-`, there must be exactly **three** parts, and the first must
  be `"CVE"`.
- The year has exactly **4** digits and is at least `1999`; the number has
  at least **4** digits. Use `isdigit()` to check the digits.

**Expected output:**

```
'CVE-2025-12345' (2025, 12345)
' cve-2019-0042 ' (2019, 42)
'CVE-25-1234' None
'CVE-2024-12a4' None
```
