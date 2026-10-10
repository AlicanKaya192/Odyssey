`flag_notes(notes, words)` should find whether **any** of the words in
`words` appears in each note, ignoring case, and return a list of `True` /
`False`. Turn the words into one pattern with `"|".join(words)`; `case=False`,
and `na=False` for a missing note. **Do not write a loop.**

**Expected output:**

```
[True, False, False, True, False]
```
