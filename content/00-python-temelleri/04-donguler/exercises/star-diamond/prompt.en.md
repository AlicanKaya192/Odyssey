For `height = 7`, draw this diamond:

```
   *
  ***
 *****
*******
 *****
  ***
   *
```

Rules:

- The diamond is `height` lines tall; `height` is always odd. Your code
  should draw the right diamond when `height` is 5 or 9 too.
- The output is compared **space for space**: the spaces at the start of
  the lines are part of the shape, and there must be none at the end.

Think about one line first: how many spaces at the start, then how many
stars? In the top half the stars **grow by two** on every line and the
spaces **shrink by one**; in the bottom half, the other way round. Once
you find how these two numbers relate to the line number, the rest is a
loop.

Multiplying a text by a number repeats it: `" " * 3` is three spaces,
`"*" * 5` five stars. Join them with `+` and print.

> Watch out: if you write `print(" " * 3, "*" * 5)`, the comma puts an
> extra space in between and the shape shifts. Join the pieces with `+`.
