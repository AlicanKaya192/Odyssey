The file `words.txt` holds accented words. `strip_accents(text)` should split
the text into letters and marks with NFD, drop the combining marks (those
where `unicodedata.combining(c)` is not zero) and return the rest joined
together.

**Expected output:**

```
cafe
naive
Angstrom
seker
Izmir
uber
facade
resume
jalapeno
creme brulee
```
