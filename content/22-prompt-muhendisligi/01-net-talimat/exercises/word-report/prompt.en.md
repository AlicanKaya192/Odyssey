`word_report(text, max_words)` should find the number of words in the text
(`text.split()`) and return `[number of words, status]`: the status is
`"ok"` if the number does not exceed the limit, `"too long"` if it
does.

**Expected output:**

```
[5, 'ok']
[6, 'too long']
```
