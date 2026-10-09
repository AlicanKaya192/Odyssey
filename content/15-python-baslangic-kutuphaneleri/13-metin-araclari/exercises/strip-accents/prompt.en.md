There is a `names.txt` with accented names next to your file; the ready
`ascii_lines` function reads the file and passes every line through
`strip_accents`.

Write the function `strip_accents(text)`: decompose the text with
`unicodedata.normalize("NFD", ...)`, drop the characters whose category is
`"Mn"` (accent marks) and join the rest.

**Expected output:**

```
Cafe Creme
Unlu Seker
Zoe Saldana
plain
```
