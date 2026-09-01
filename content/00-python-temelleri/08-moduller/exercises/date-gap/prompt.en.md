The `datetime` module is for working with dates. In this exercise you will
find the number of days between two dates.

**What you need to do:**

1. Take the `date` class from the `datetime` module:
   `from datetime import date`
2. Define two dates:
   - `start` — 1 January 2026
   - `end` — 1 March 2026
3. Hold the **number of days** between them in a variable called `gap`.
4. Hold the text form of `start` in a variable called `label`.
5. Print `gap` first, then `label`.

**Expected output:**

```
59
2026-01-01
```

> Subtracting two dates gives you a `timedelta`; the number of days is in its
> `.days` attribute. `.isoformat()` gives you the text form of a date.
