In the United States it is customary to leave a tip for your server, typically 15% or more of the meal's cost. We have written most of a tip calculator for you (the starter code), but did not have time to implement two functions:

- `dollars_to_float(d)`: accept a `str` formatted as `$##.##` (each `#` a digit), remove the leading `$` and return the amount as a `float`. For `"$50.00"`, `50.0`.
- `percent_to_float(p)`: accept a `str` formatted as `##%`, remove the trailing `%` and return the percentage as a `float`. For `"15%"`, `0.15`.

Assume the user will input values in the expected formats. Do not change `main`. (In CS50 the file is `tip.py`.)

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `$50.00`, `15%` → output `Leave $7.50`
- Input `$100.00`, `18%` → output `Leave $18.00`
- Input `$15.00`, `25%` → output `Leave $3.75`
