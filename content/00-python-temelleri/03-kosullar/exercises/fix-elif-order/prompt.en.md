The starting code turns an exam score into a letter grade: 90 and above
`A`, 80 and above `B`, 70 and above `C`, 50 and above `D`, below that `F`.

The code runs, but for a score of `85` it prints `D` instead of `B`. Find
the mistake and fix it; do not change `score`. Once fixed, the output is:

```
B
```

Think about this: an `elif` chain is read from top to bottom and stops at
the **first** condition that holds; the ones below are never looked at.
Where does 85 hold for the first time?

> Watch out: you do not need to touch the conditions; each of them is
> right on its own. The problem is their order.
