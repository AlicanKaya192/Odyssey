The three tests in `test_main.py` pass one by one, but two of them fail
when run together: the `books` dictionary is shared between tests.

**What to do:** without touching the tests, add an `autouse` fixture that
clears `books` before (and after) every test.
