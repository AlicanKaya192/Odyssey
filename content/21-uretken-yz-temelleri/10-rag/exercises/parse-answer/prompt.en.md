`parse_answer(text)` should find the source numbers of the form `[n]` in the
answer and return `[text without numbers, list of the numbers as ints]`. The
text without numbers is the text with the numbers removed and the leading and
trailing spaces stripped.

**Expected output:**

```
['Valid for 3 years.', [1]]
['Open 9:00 and online.', [2, 3]]
```
