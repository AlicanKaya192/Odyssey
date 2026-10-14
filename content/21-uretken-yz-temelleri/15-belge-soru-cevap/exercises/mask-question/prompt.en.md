`mask_count(text)` should apply the lesson's three patterns (`EMAIL`,
`PHONE`, `ORDER`) in turn and return `[masked text, total number of pieces
masked]`. `re.subn` can be used for the count: it gives the changed text and
the number of replacements together.

**Expected output:**

```
['Mail [EMAIL], [ORDER]', 2]
```
