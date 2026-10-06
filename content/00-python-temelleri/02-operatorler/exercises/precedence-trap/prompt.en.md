All three lines in the starting code run, but they give the **wrong
result**. Above each line it says what should be calculated. Without
touching the numbers, fix them by **adding parentheses** only.

Once fixed, the output should be:

```
80.0 4 8
```

Python does not work from left to right; it follows an order of
precedence:

1. `**` (power) first
2. Then the sign: a minus like `-2`
3. Then `*`, `/`, `//`, `%`
4. `+` and `-` last (left to right among themselves)

Parentheses come before everything.

> Watch out: many people are surprised that `-2 ** 2` gives `-4`, not
> `4`: Python works out `2 ** 2` first and applies the minus afterwards.
