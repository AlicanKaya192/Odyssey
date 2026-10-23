Reimplement **Home Federal Savings Bank** from Problem Set 1: the work of finding the amount happens in a function, `value(greeting)`. `value` takes a string and returns an **int**: `0` if the greeting starts with `hello`, `20` if it starts with `h` (but not `hello`), `100` otherwise. It is case-insensitive; you may assume the string has no leading spaces (`main` strips them). `main` prints the amount as `$20`.

Then, in `test_bank.py`, write **three or more** functions whose names start with `test_` that test `value` thoroughly.

## How to test

The cases for your program; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `Hello` → output `$0`
- Input `Hello, Newman` → output `$0`
- Input `How you doing?` → output `$20`
- Input `What's happening?` → output `$100`
- Input `   hey` → output `$20`

For your tests: Odyssey first runs `test_bank.py` with **your** `bank.py` (all tests must pass), then with deliberately broken versions of `bank.py` (with each one, at least one of your tests must fail). CS50's check50 checks tests the same way.
