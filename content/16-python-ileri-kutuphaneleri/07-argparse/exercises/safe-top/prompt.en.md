Write the function `safe_top(argv)`: build a parser with
`exit_on_error=False` and define a `--top` of type `int` (default 5). If
parsing succeeds, return the `top` value; if an `ArgumentError` comes, return
the text `"invalid"`; the program must not exit.

**Expected output:**

```
3 invalid 5
```
