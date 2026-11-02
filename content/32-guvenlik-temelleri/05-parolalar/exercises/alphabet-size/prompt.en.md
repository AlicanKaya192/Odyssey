Let us estimate the size of the alphabet an attacker has to try by
looking at which kinds of characters a password contains:

- `26` if it has a lower-case letter, `26` if it has an upper-case letter,
  `10` if it has a digit,
- `32` if it has any other character (a symbol, a space).

`alphabet_size(password)` should return the sum for the kinds found. Each
kind is counted once. `str.islower()`, `isupper()`, `isdigit()` also work
on a single character.

**Expected output:**

```
hello 26
Hello 52
Hello1 62
Hello1! 94
1234 10
```
