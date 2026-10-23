Fuel gauges often show with fractions how much fuel is in a tank: `1/4` means the tank is 25% full, `1/2` 50%, `3/4` 75%.

Implement a program that prompts the user for a fraction formatted as `X/Y`, where `X` is a non-negative integer and `Y` a positive integer, and outputs, as a percentage **rounded to the nearest integer**, how much fuel is in the tank (`75%`). If 1% or less remains (the tank is essentially empty), output `E` instead; if 99% or more remains (essentially full), output `F`.

If `X` or `Y` is not an integer, `X` is greater than `Y`, or `Y` is 0, **prompt the user again**. Be sure to catch exceptions like `ValueError` or `ZeroDivisionError`. (In CS50 the file is `fuel.py`.)

Hint: one `except` can catch several types: `except (ValueError, ZeroDivisionError):`. `round` rounds to the nearest integer.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `3/4` → output `75%`
- Input `1/4` → output `25%`
- Input `4/4` → output `F`
- Input `0/4` → output `E`
- Input `4/0`, `1/2` → output `50%`
- Input `three/four`, `1/2` → output `50%`
- Input `1.5/3`, `1/2` → output `50%`
- Input `-3/4`, `1/2` → output `50%`
- Input `5/4`, `1/2` → output `50%`
- Input `2/3` → output `67%`
- Input `99/100` → output `F`
- Input `1/100` → output `E`
