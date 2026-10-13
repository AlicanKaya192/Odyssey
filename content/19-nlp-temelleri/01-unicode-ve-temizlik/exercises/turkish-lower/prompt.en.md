Each line of the file `pairs.txt` holds an upper-case Turkish word and its
correct lower-case form. `turkish_lower(text)` should first turn `I` into
`ı` and `İ` into `i`, then apply `lower()`. The starter code uses plain
`lower()`; some lines come out `False`.

You do not need to type Turkish letters: `chr(0x131)` is "ı", `chr(0x130)`
is "İ".

**Expected output:**

```
True
True
True
True
True
True
True
True
```
