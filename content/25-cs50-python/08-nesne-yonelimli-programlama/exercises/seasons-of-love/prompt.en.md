A year is 525,600 minutes, as in the song. Ask the user for their date of birth in `YYYY-MM-DD` form (`1999-01-01`) and print, **in words**, in English, how many minutes have passed from that day until today: `Five hundred twenty-five thousand, six hundred minutes`. Assume the person was born at midnight and that it is now midnight today; so the number of days × 24 × 60. `inflect` turns the number into words (`p.number_to_words(n, andword="")`: no `and` in between, as CS50 asks); the result starts with a capital letter and ends with ` minutes`.

Put the work in two functions:

- `minutes_between(birth, today)`: takes two date strings and returns the minutes between them as an int. If a date is invalid (`January 1, 1999`, `1999-02-30`), it raises a `ValueError`; `date.fromisoformat` already does that.
- `sing(minutes)`: turns the minutes into words and returns them.

`main` asks for the date of birth, passes today as `date.today().isoformat()` and prints the result; if the date is invalid, it exits with `sys.exit("Invalid date")` instead of raising an error. (We made `today` a parameter so the tests give the same result every day.)

Then, in `test_seasons.py`, write functions whose names start with `test_` that test the two functions other than `main` thoroughly.

## How to test

The cases for your program; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `January 1, 1999` → output (nothing) (exit code 1)
- Input `1999-02-30` → output (nothing) (exit code 1)
- Input `cat` → output (nothing) (exit code 1)

For your tests: Odyssey first runs `test_seasons.py` with **your** `seasons.py` (all tests must pass), then with deliberately broken versions of `seasons.py` (with each one, at least one of your tests must fail). CS50's check50 checks tests the same way.
