We want to count the "um"s in someone's speech. In `um.py`, write `count(s)`: it takes a string and returns, as an int, how many times `um` appears in it **as a word of its own**, case-insensitively. An `um` inside another word does not count: there is none in `yummy`, `album` or `umbrella`. `main` asks for the text and prints the result.

Then, in `test_um.py`, write **three or more** functions whose names start with `test_` that test `count` thoroughly.

## How to test

The cases for your program; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `hello, um, world` → output `1`
- Input `Um, thanks for the album.` → output `1`
- Input `Um, thanks, um...` → output `2`
- Input `yummy` → output `0`

For your tests: Odyssey first runs `test_um.py` with **your** `um.py` (all tests must pass), then with deliberately broken versions of `um.py` (with each one, at least one of your tests must fail). CS50's check50 checks tests the same way.
