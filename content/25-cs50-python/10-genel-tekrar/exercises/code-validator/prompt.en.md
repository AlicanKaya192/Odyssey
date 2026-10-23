Product codes in a warehouse follow this rule: two **uppercase** letters, a hyphen, four digits; the first digit can't be 0 (`AB-1234` is valid; `AB-0123`, `ab-1234`, `AB1234`, `AB-12345` are invalid). Nothing else may come before or after the code. In `validate.py`, `is_valid(code)` checks this with a regular expression and returns `True` or `False`; `main` asks for the code and prints `Valid` or `Invalid`.

Then, in `test_validate.py`, write functions whose names start with `test_` that test `is_valid`.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python validate.py
Code: AB-1234
Valid
```

For your tests: Odyssey first runs `test_validate.py` with **your** `validate.py` (all tests must pass), then with deliberately broken versions of `validate.py` (with each one, at least one of your tests must fail).
