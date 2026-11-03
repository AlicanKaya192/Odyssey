A product code is two capital letters, a hyphen and four digits
(`AB-1234`). `valid_code(code)` should return `True` if the whole code has
this form. The starter code uses `re.match` and `^...$`; it accepts a code
with a newline at the end.

**Expected output:**

```
'AB-1234' True
'ab-1234' False
'AB-1234\n' False
'AB-12345' False
```
