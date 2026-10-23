An **IPv4 address** is four numbers separated by periods, `#.#.#.#`, each between 0 and 255 (`255.255.255.255` is valid, `512.512.512.512` is not). In `numb3rs.py`, write `validate(ip)`: it takes a string and returns `True` if it is a valid IPv4 address, otherwise `False`. `main` asks for the address and prints `validate`'s result (`True` or `False`). Checking the numbers' range with a pattern is hard; check the format with a pattern and the range with `int`.

Then, in `test_numb3rs.py`, write **two or more** functions whose names start with `test_` that test `validate` thoroughly.

## How to test

The cases for your program; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `127.0.0.1` → output `True`
- Input `255.255.255.255` → output `True`
- Input `512.512.512.512` → output `False`
- Input `1.2.3.1000` → output `False`
- Input `cat` → output `False`

For your tests: Odyssey first runs `test_numb3rs.py` with **your** `numb3rs.py` (all tests must pass), then with deliberately broken versions of `numb3rs.py` (with each one, at least one of your tests must fail). CS50's check50 checks tests the same way.
