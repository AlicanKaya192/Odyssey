In `working.py`, write `convert(s)`: it takes two times in 12-hour form, `9:00 AM to 5:00 PM` or briefly `9 AM to 5 PM`, and returns them in 24-hour form: `09:00 to 17:00`. The two times may have different forms (`9 AM to 5:30 PM`). `AM` and `PM` are uppercase, with a space before each. Do not assume the work starts in the morning: `10 PM to 8 AM` → `22:00 to 08:00`. `12 AM` is midnight (`00:00`), `12 PM` noon (`12:00`). If either time is invalid (`9:60 AM`, `13 PM`) or the input is not in this form (`9 AM - 5 PM`), raise a `ValueError`; do not catch it, let the program crash. `main` asks for the hours and prints `convert`'s result.

Then, in `test_working.py`, write **three or more** functions whose names start with `test_` that test `convert` thoroughly.

## How to test

The cases for your program; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `9 AM to 5 PM` → output `09:00 to 17:00`
- Input `9:00 AM to 5:00 PM` → output `09:00 to 17:00`
- Input `10 PM to 8 AM` → output `22:00 to 08:00`
- Input `10:30 PM to 8:50 AM` → output `22:30 to 08:50`

For your tests: Odyssey first runs `test_working.py` with **your** `working.py` (all tests must pass), then with deliberately broken versions of `working.py` (with each one, at least one of your tests must fail). CS50's check50 checks tests the same way.
