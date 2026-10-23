In the United States, dates are typically written in month-day-year order (`MM/DD/YYYY`). That format cannot be sorted easily (the year comes last) and is ambiguous: Harvard was founded on September 8, 1636, but `9/8/1636` could also be read as August 9, 1636. Computers instead use ISO 8601: year-month-day (`YYYY-MM-DD`), four digits for the year and two for the month and day, padded with leading zeroes as needed.

Implement a program that prompts the user for a date in month-day-year order, formatted like `9/8/1636` or `September 8, 1636`, where the month name is one of the `months` list in the starter code. Output the same date as `YYYY-MM-DD`. If the input is not a valid date in either format, **prompt the user again**. Assume every month has no more than 31 days; no need to check for 28, 29 or 30. (In CS50 the file is `outdated.py`.)

Hint: `months.index("September")` gives `8` (a name not in the list raises a `ValueError`). In an f-string, `{month:02}` writes the number with two digits, padded with a zero.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `9/8/1636` → output `1636-09-08`
- Input `September 8, 1636` → output `1636-09-08`
- Input `23/6/1912`, `6/23/1912` → output `1912-06-23`
- Input `December 80, 1980`, `12/25/1980` → output `1980-12-25`
- Input `September 8 1636`, `1/1/2000` → output `2000-01-01`
- Input `  10/9/1701 ` → output `1701-10-09`
- Input `Octobr 9, 1701`, `October 9, 1701` → output `1701-10-09`
