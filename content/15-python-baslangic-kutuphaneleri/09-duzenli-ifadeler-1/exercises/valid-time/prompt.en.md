Write the function `valid_time(text)`: return `True` if the text is in the
format `"HH:MM"` (two digits, a colon, two digits: `re.fullmatch`) **and**
the hour is below 24 and the minute below 60; otherwise `False`. Let the
regex check the form and Python the meaning.

**Expected output:**

```
09:30 True
23:59 True
24:00 False
7:15 False
12:60 False
```
