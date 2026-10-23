In Massachusetts, home to Harvard University, you can request a vanity license plate with your choice of letters and numbers. Among the requirements:

- All vanity plates must start with at least two **letters**.
- At least 2 and at most 6 characters (letters or numbers).
- Numbers cannot be used in the middle; they must come at the end: `AAA222` is acceptable, `AAA22A` is not. The first number used cannot be a `0`.
- No periods, spaces or punctuation marks.

Implement a program that prompts the user for a vanity plate and outputs `Valid` if it meets all of the requirements or `Invalid` if it does not. Assume any letters will be uppercase. Structure your program as in the starter code: `is_valid(s)` returns `True` if all requirements are met and `False` otherwise. You may write one function per requirement if you like. (In CS50 the file is `plates.py`.)

Hint (from CS50): strings have the methods `isalpha` (all letters?), `isdigit` (all digits?) and `isalnum` (all letters or digits?); `s[0]` is the first character.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `CS50` → output `Valid`
- Input `CS05` → output `Invalid`
- Input `CS50P` → output `Invalid`
- Input `PI3.14` → output `Invalid`
- Input `H` → output `Invalid`
- Input `OUTATIME` → output `Invalid`
- Input `AAA222` → output `Valid`
- Input `AAA22A` → output `Invalid`
- Input `50CS` → output `Invalid`
- Input `NRVOUS` → output `Valid`
