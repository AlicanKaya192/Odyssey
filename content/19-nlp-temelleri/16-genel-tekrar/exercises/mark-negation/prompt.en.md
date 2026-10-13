A bag of words cannot see negation. A classic trick: put `NOT_` in front of the
tokens after a negator. `mark_negation(tokens)`:

- a token from `NEGATORS` **opens** the mark (it stays unchanged),
- a token from `PUNCT` **closes** the mark (it stays unchanged),
- while the mark is open other tokens get the `NOT_` prefix.

**Expected output:**

```
it is not NOT_good NOT_at NOT_all . love it
```
