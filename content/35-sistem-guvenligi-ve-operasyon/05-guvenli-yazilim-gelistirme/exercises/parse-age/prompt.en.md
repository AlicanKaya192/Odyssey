`parse_age(text)` should validate an age from a form field with an allow
list: if the text consists only of **1 to 3 digits** and the value does not
exceed 150, return the number, otherwise `None`. It must not raise an
error on any input. Hint: `re.fullmatch(r"[0-9]{1,3}", text)`.

**Expected output:**

```
'42' 42
'150' 150
'151' None
'-3' None
'abc' None
'' None
```
