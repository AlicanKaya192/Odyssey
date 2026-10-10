`split_codes(codes)` should take apart codes like `"TR-34-0012"` with
`str.extract`: two capital letters (country), two digits (region), four digits
(number). Codes that do not fit are dropped (`dropna()`). Return:

- `"country"`: the countries (a list)
- `"num"`: the numbers as **integers** (`astype(int)`)

**Do not write a loop.**

**Expected output:**

```
['TR', 'TR', 'DE']
[12, 450, 7]
```
