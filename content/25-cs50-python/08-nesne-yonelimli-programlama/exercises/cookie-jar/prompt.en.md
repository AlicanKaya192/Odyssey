Represent a cookie jar with a class. The skeleton of the `Jar` class in `jar.py` is the one CS50 gives; do not change the parameters, but you may add methods of your own.

- `__init__(capacity=12)`: the most cookies the jar can hold. If `capacity` is not a non-negative `int`, `ValueError`. The jar starts empty.
- `__str__`: one `🍪` per cookie in the jar; `🍪🍪🍪` for 3 cookies. The emoji is not on your keyboard; use the `COOKIE` constant in the starter code (`COOKIE * 3`).
- `deposit(n)`: adds `n` cookies; `ValueError` if that would exceed the capacity.
- `withdraw(n)`: removes `n` cookies; `ValueError` if there are fewer than `n` in the jar.
- `capacity` (property): the capacity.
- `size` (property): the number of cookies in the jar.

Then, in `test_jar.py`, write **four or more** functions whose names start with `test_` that test `Jar` thoroughly (like `test_init`, `test_str`, `test_deposit`, `test_withdraw`). Use `COOKIE` when comparing cookies too: `assert str(jar) == COOKIE * 3`.

## How to test

The cases for your program; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.



For your tests: Odyssey first runs `test_jar.py` with **your** `jar.py` (all tests must pass), then with deliberately broken versions of `jar.py` (with each one, at least one of your tests must fail). CS50's check50 checks tests the same way.
