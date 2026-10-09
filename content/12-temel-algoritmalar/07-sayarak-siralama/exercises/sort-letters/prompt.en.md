Write the function `sort_letters(word)`: for a word made only of lowercase
English letters (`a`–`z`), it returns its letters in alphabetical order as a
string.

- `sort_letters("banana")` → `"aaabnn"`

Use a list of 26 counters: `ord(letter) - ord("a")` gives the letter's
position (0–25), `chr(index + ord("a"))` turns it back into a letter. Do not
use `sorted` or `.sort()`.

**Expected output:**

```
aaabnn
aghilmort
```
