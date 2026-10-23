`dates_in(text, policy)` should find all `DD/DD/YYYY` dates in the text (two
digits, two digits, four digits, with word boundaries) in order and return
one result for each:

- If `policy` is `"US"`, the first number is the month; if `"day-first"`,
  the first number is the day.
- If `policy` is `None`: when both numbers are 12 or less and different,
  `"needs_clarification"`; otherwise the one above 12 is the day (if they
  are equal it does not matter).
- The result is a date like `"2026-03-04"`; if no such day exists (month 13,
  31 February), `"rejected"`.

**Expected output:**

```
['2026-03-04', 'rejected']
['needs_clarification', '2026-04-13']
```
