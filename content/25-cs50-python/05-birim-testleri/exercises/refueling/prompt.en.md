Reimplement **Fuel Gauge** from Problem Set 3, split into three functions:

- `convert(fraction)`: takes a string formatted as `X/Y` (`X` a non-negative and `Y` a positive integer) and **returns** the fraction as a percentage rounded to the nearest int (between 0 and 100). If `X` or `Y` is not an integer, or `X` is greater than `Y`, it raises a `ValueError`; if `Y` is 0, a `ZeroDivisionError` (`raise ValueError`).
- `gauge(percentage)`: takes an int; returns `"E"` if it is 1 or less, `"F"` if 99 or more, otherwise the number followed by `%` (`"75%"`) as a string.
- `main`: asks until a valid fraction arrives and prints `gauge`'s result. Only `main` calls `print`.

Then, in `test_fuel.py`, write **two or more** functions whose names start with `test_` that test `convert` and `gauge` thoroughly. For the cases that should raise an error, `pytest.raises`.

## How to test

The cases for your program; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `3/4` → output `75%`
- Input `1/100` → output `E`
- Input `99/100` → output `F`
- Input `cat`, `5/4`, `1/0`, `1/2` → output `50%`

For your tests: Odyssey first runs `test_fuel.py` with **your** `fuel.py` (all tests must pass), then with deliberately broken versions of `fuel.py` (with each one, at least one of your tests must fail). CS50's check50 checks tests the same way.
