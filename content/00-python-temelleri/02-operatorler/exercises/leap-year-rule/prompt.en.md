Find out whether a year is a leap year (when February has 29 days) with
**a single logical expression**, and put it in the variable `is_leap`:

```
1900 is a leap year: False
```

The rule has three parts:

1. Years divisible by 4 are leap years…
2. …but those divisible by 100 are **not**…
3. …but those divisible by 400 **are** leap years again.

So `2024` is a leap year, `1900` is not (divisible by 100), `2000` is
(divisible by 400).

"Divisible" is checked with `%`: `year % 4 == 0`. Combine the parts with
`and`, `or` and parentheses where needed.

Your code should give `False` for `1900`. When it does, change `year` to
`2000`, `2024` and `2023` and try: you should get `True`, `True`, `False`.
Then set it back to `1900`.

> Watch out: if you only write `year % 4 == 0`, you get `True` for `1900`
> too. All three parts of the rule must be in the expression.
