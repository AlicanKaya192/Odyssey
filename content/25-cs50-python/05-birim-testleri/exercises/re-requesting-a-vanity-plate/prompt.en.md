Reimplement **Vanity Plates** from Problem Set 2. The requirements are the same:

- It starts with at least two **letters**.
- At least 2 and at most 6 characters.
- Numbers cannot be in the middle, they come at the end (`AAA222` is fine, `AAA22A` is not); the first number cannot be `0`.
- No periods, spaces or punctuation.

`is_valid(s)` returns `True` if all requirements hold and `False` otherwise; only `main` prints. `main` is called when the file runs directly (`if __name__ == "__main__":`). Assume the letters are uppercase.

Then, in `test_plates.py`, write **four or more** functions whose names start with `test_` that test `is_valid` thoroughly. Each broken version forgets one of the requirements; try every requirement with its own example.

## How to test

The cases for your program; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `CS50` → output `Valid`
- Input `CS05` → output `Invalid`
- Input `PI3.14` → output `Invalid`
- Input `H` → output `Invalid`
- Input `OUTATIME` → output `Invalid`

For your tests: Odyssey first runs `test_plates.py` with **your** `plates.py` (all tests must pass), then with deliberately broken versions of `plates.py` (with each one, at least one of your tests must fail). CS50's check50 checks tests the same way.
