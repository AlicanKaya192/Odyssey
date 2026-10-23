The most common mistakes when writing tests and their messages (measured with
Python 3.14 and pytest). We shortened the version lines at the top of the
output and the time at the end.

## An unconditional main() at the end of the module

If `calculator.py` ends with an unconditional `main()`:

```python
def main():
    x = int(input("What's x? "))
    print("x squared is", square(x))


def square(n):
    return n * n


main()
```

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 0 items / 1 error

========================= ERRORS ==========================
___________ ERROR collecting test_calculator.py ___________
test_calculator.py:1: in <module>
    from calculator import square
calculator.py:10: in <module>
    main()
calculator.py:2: in main
    x = int(input("What's x? "))
            ^^^^^^^^^^^^^^^^^^^
...\site-packages\_pytest\capture.py:229: in read
    raise OSError(
E   OSError: pytest: reading from stdin while output is captured!  Consider using `-s`.
--------------------- Captured stdout ---------------------
What's x? 
================= short test summary info =================
ERROR test_calculator.py - OSError: pytest: reading from ...
!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!
========================= 1 error =========================
```

When the test file imported `square`, `calculator.py` ran from top to bottom,
`main` was called too, and `input` waited for input. `pytest` gives no input
while it runs tests, so it stopped. The fix: put the last line inside
`if __name__ == "__main__":`.

## A function whose name does not start with test_

```python
from calculator import square


def positive():
    assert square(2) == 4
    assert square(3) == 9


def negative():
    assert square(-2) == 4
    assert square(-3) == 9


def zero():
    assert square(0) == 0
```

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 0 items

======================= no tests ran ======================
```

No error, but no test ran either (`no tests ran`). `pytest` counts only
functions whose names start with `test_` as tests.

## A function that prints but does not return

If a function prints its result with `print`, its value is `None`, and
`assert hello("David") == "hello, David"` fails like this:
`assert None == 'hello, David'`. Even if the program seems to work, it cannot
be tested. Let the function `return` and `main` print.

## Mistakes that raise no error

A passing test does not prove the code is right; it only shows it is right for
the cases you tried. With a `calculator.py` that has `+` instead of `*`:

```python
from calculator import square


def test_square():
    assert square(2) == 4
```

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 1 item

test_calculator.py .                                 [100%]

========================= 1 passed ========================
```

The test passed, because `2 + 2` is also 4. Only a case that gives the wrong
code away catches it: 3, negative numbers. That is why Odyssey also runs your
tests against broken versions.
