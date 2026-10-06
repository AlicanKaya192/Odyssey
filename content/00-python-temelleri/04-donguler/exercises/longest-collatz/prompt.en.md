Start with a number and apply this rule:

- If the number is **even**, divide it by two.
- If the number is **odd**, multiply it by three and add one.

Repeat until the number is `1`. For example `6`: 6 → 3 → 10 → 5 → 16 → 8 →
4 → 2 → 1. That journey took **8 steps**. Whatever number you start with,
you always seem to reach 1 (this is called the Collatz conjecture; nobody
has proved it yet).

Among the starting numbers from `1` to `30` (30 included), **which one has
the longest journey**? Put the start in `best_start` and the number of
steps in `best_steps`:

```
Longest: 27 with 111 steps
```

Two loops, one inside the other:

- The outer `for` loop tries every starting number from 1 to 30.
- The inner `while` loop runs that number's journey and counts the steps.
  How many times it will repeat is not known in advance; that is exactly
  what `while` is for.

> Watch out: do not change the starting number in the inner loop; work
> with a copy (`n = start`). Otherwise the outer loop loses track of
> which number it is on. Reset the step counter for every new start too.
