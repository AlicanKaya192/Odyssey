Reimplement **Just setting up my twttr** from Problem Set 2: this time the work of omitting vowels (A, E, I, O, U, uppercase or lowercase) happens in a function, `shorten(word)`. `shorten` takes a string and **returns** it with its vowels omitted (`return`), without printing; only `main` calls `print`. The structure in the starter code is the one CS50 asks for: `main`, `shorten` and `if __name__ == "__main__":` at the end.

Then, in `test_twttr.py`, write one or more functions whose names start with `test_` that test `shorten` thoroughly. `from twttr import shorten` is ready.

## How to test

The cases for your program; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `Twitter` → output `Twttr`
- Input `What's your name?` → output `Wht's yr nm?`
- Input `CS50` → output `CS50`

For your tests: Odyssey first runs `test_twttr.py` with **your** `twttr.py` (all tests must pass), then with deliberately broken versions of `twttr.py` (with each one, at least one of your tests must fail). CS50's check50 checks tests the same way.
