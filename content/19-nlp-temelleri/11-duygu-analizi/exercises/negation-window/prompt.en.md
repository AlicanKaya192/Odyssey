`negated(text, window)` should apply the negation rule of the lesson. Take the
tokens with `re.findall(r"[a-z']+|[.,!?]", text.lower())`:

- A punctuation mark closes the window.
- A word from `NEGATORS` opens the window for `window` words and scores
  nothing itself.
- Other words score `GOOD` +1, `BAD` −1; if the window is open the sign is
  flipped and the window shrinks by one word.

**Expected output:**

```
-1
2
1
```
