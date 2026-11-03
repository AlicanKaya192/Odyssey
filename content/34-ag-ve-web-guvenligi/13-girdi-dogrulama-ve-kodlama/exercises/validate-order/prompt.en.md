`validate(form)` should return the names of the wrong fields as a list
**in this order**: `zip` if it is not exactly 5 digits; `qty` if it is not
1–2 digits or not between 1 and 99; `color` if it is not in `COLORS`. A
missing field is wrong too. Use `re.fullmatch` for the form.

**Expected output:**

```
[]
['zip', 'qty', 'color']
['zip']
```
