`fit_middle(text, max_words)` should return the text as it is if it does
not exceed `max_words` words. If it does, keep the first
`max_words // 2` words and the last `max_words - max_words // 2` words
with `" ... "` between them. Words are split with `text.split()` and
joined with single spaces.

**Expected output:**

```
one two ... six seven
short text
```
