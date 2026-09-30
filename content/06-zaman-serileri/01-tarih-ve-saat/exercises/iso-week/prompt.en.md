A weekly report assigns each date to a week labelled `YEAR-Wweek`,
such as `2024-W10`. Dates at the turn of the year are a trap.

```python
days = ["2024-03-09", "2024-12-29", "2024-12-30", "2025-01-01", "2021-01-01"]
```

**What to do:**

1. Turn each text into a date with `date.fromisoformat`.
2. Get the year and week number with `isocalendar()`.
3. Print the date and the label on each line. The label has a two-digit week
   number: `f"{year}-W{week:02d}"`.

**Expected output:**

```
2024-03-09 2024-W10
2024-12-29 2024-W52
2024-12-30 2025-W01
2025-01-01 2025-W01
2021-01-01 2020-W53
```

30 December 2024 and 1 January 2025 are in the same week: week 1 of 2025.
1 January 2021 is week 53 of 2020. Had you taken the year from `d.year`,
these rows would have gone to the wrong year.
