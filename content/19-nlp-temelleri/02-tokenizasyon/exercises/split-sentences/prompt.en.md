`split_sentences(text)` should first split as in the lesson with
`re.split(r"(?<=[.!?])\s+", text)`. Then walk the pieces in order: if the
**last word** of the previous sentence (lowercased) is in `ABBREVIATIONS`,
join the new piece to it with a space; otherwise add it to the list as a new
sentence.

**Expected output:**

```
Dr. Lee paid $4.50 today.
Great service!
Ask Mr. Kim, e.g. by mail.
Done?
```
