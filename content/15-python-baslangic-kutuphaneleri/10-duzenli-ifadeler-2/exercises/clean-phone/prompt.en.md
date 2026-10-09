Write the function `clean_phone(text)`: delete everything that is not a
digit (`re.sub(r"\D", "", text)`); if what is left is **11 digits** starting
with `0`, return it, otherwise `None`. So `"0532 123 45 67"` and
`"(0532) 123-4567"` come down to the same number.

**Expected output:**

```
05321234567
05321234567
None
05321234567
```
