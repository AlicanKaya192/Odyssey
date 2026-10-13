`tokenize(text)` should lowercase the text and split it with
`re.findall(r"\w+|[^\w\s]", ...)`: runs of letters and digits, and single
punctuation marks. The starter code uses `split()`; punctuation stays glued
to the words.

**Expected output:**

```
hello|,|world|!|it|'|s|5pm|.
fast|delivery|.|.|.
```
