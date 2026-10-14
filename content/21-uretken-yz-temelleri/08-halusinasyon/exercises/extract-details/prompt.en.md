`details(text)` should return the numbers (times like `9:00` included) and the
words starting with a capital letter in the order found; but it should not
put the sentence's **first word** (with a trailing `,` or `.` removed) in the
list. The regex: `r"\d+(?::\d+)?|[A-Z][a-z]+"`.

**Expected output:**

```
['Monday', 'Friday', '9:00', '17:00']
['Canada', '10']
```
