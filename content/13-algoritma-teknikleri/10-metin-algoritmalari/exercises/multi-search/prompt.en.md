Write the function `multi_search(text, patterns)`: all patterns have the
**same length**. For each match in the text it returns a `(position, pattern)`
tuple, in a list sorted by position.

The Rabin-Karp idea: put the patterns in a **set**, look up each window of the
text in the set (a Python set uses a hash behind the scenes). This way each
window is a single lookup, whatever the number of patterns.

**Expected output:**

```
(4, 'cat')
(19, 'mat')
(30, 'hat')
```
