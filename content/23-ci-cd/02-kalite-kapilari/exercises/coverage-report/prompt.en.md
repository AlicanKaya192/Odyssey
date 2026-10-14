The two questions of a coverage tool: which lines never ran, and what percentage ran?

Write two functions. `ran` is the list of lines that ran, `body` the list of all measured lines:

- `missed_lines(ran, body)`: the lines that are in `body` but not in `ran`, in `body`'s order.
- `coverage_percent(ran, body)`: the percentage of lines that ran, rounded to a whole number with `round`. If `body` is empty, `100`.

The lesson's measurement: `ran = [2, 4, 5, 7]`, `body = [2, 3, 4, 5, 6, 7]` → missed `[3, 6]`, `67`.

**Expected output:**

```
[3, 6]
67
100
100
```
