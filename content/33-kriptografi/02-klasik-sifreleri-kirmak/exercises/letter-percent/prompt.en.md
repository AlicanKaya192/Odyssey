`letter_percent(text, n)` should count the letters in the text (case
does not matter, non-letters are not counted) and return the `n` most
common as `[letter, percent]`. Percent is `round(100 * count /
total_letters, 1)`. Order: count from high to low, ties in alphabetical
order.

**Expected output:**

```
l 33.3
o 20.0
e 13.3
[['a', 50.0], ['b', 50.0]]
```
