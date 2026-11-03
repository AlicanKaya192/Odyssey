`parse_security_txt(text)` should read every `Field: value` line and
return a dict of field name (lower case) → list of values. Blank lines,
comment lines starting with `#` and lines with no colon are skipped. The
value is split only at the first colon.

**Expected output:**

```
contact 2
expires 1
```
