# Unit Tests

The sixth week of CS50 Python. You can watch the video in the **Video** tab;
this page is the written version of the lecture. Up to now you have probably checked
your code with `print` lines or with Odyssey's checks. Programmers usually
write **code that tests their own programs**: these are called **tests**. A
test that checks one small part of a program, usually a single function, is a
**unit test**.

## The program to test

A small program that squares a number, `calculator.py`:

```python
def main():
    x = int(input("What's x? "))
    print("x squared is", square(x))


def square(n):
    return n * n


if __name__ == "__main__":
    main()
```

```text
$ python calculator.py
What's x? 2
x squared is 4
```

`square(2)` gave 4, which looks right. But what about 3, negative numbers, 0?
Instead of running the program and typing a number by hand each time, we will
write a program that tries `square` by itself.

## Keeping main from running on import

The last two lines of `calculator.py` are new:

```python
if __name__ == "__main__":
    main()
```

Python gives every file a hidden variable called `__name__`. If you run the
file directly (`python calculator.py`), its value is `"__main__"`. If the file
is **imported** from another program (`from calculator import square`), its
value is the module's name, `"calculator"`. Thanks to this `if`, `main` is
called only when the file runs directly; when our test imports `square`, the
program does not start asking the user `What's x?`. What happens when you
forget this line is in the **Common Mistakes** note.

## A first test program

By convention a test file's name starts with `test_` followed by the name of
the file it tests: `test_calculator.py`. Inside, a function that calls
`square` with a few numbers and compares the result with what we expect:

```python
from calculator import square


def main():
    test_square()


def test_square():
    if square(2) != 4:
        print("2 squared was not 4")
    if square(3) != 9:
        print("3 squared was not 9")


if __name__ == "__main__":
    main()
```

```text
$ python test_calculator.py
```

It printed nothing: both comparisons held. To see that the test is useful,
let's put a bug into `calculator.py` on purpose, `+` instead of `*`:

```python
def main():
    x = int(input("What's x? "))
    print("x squared is", square(x))


def square(n):
    return n + n


if __name__ == "__main__":
    main()
```

```text
$ python test_calculator.py
3 squared was not 9
```

Since `2 + 2` is also 4, the first comparison **could not see** the bug; the
second one did. First lesson: one example is not enough.

## assert

Python's `assert` statement asserts that a condition is true. If the
condition is false, the program stops with an `AssertionError`. Instead of
`if` and `print`:

```python
from calculator import square


def main():
    test_square()


def test_square():
    assert square(2) == 4
    assert square(3) == 9


if __name__ == "__main__":
    main()
```

With the buggy `calculator.py`:

```text
$ python test_calculator.py
Traceback (most recent call last):
  File "test_calculator.py", line 14, in <module>
    main()
    ~~~~^^
  File "test_calculator.py", line 5, in main
    test_square()
    ~~~~~~~~~~~^^
  File "test_calculator.py", line 10, in test_square
    assert square(3) == 9
           ^^^^^^^^^^^^^^
AssertionError
```

The error shows which line did not hold: `assert square(3) == 9`. But the
program stopped at the first failing `assert`; if we added more cases, it
would never try the rest. Wrapping each one in `try` and `except` is one fix:

```python
from calculator import square


def main():
    test_square()


def test_square():
    try:
        assert square(2) == 4
    except AssertionError:
        print("2 squared was not 4")
    try:
        assert square(3) == 9
    except AssertionError:
        print("3 squared was not 9")
    try:
        assert square(-2) == 4
    except AssertionError:
        print("-2 squared was not 4")
    try:
        assert square(-3) == 9
    except AssertionError:
        print("-3 squared was not 9")
    try:
        assert square(0) == 0
    except AssertionError:
        print("0 squared was not 0")


if __name__ == "__main__":
    main()
```

```text
$ python test_calculator.py
3 squared was not 9
-2 squared was not 4
-3 squared was not 9
```

Now every case is tried, but five lines of work became twenty, and each new
case needs four more. There is a library that does this repetition for us.

## pytest

`pytest` is a third-party library for testing functions. On your own computer
you install it with `pip install pytest`; in Odyssey it is installed, and in
the exercises Odyssey runs your tests itself. With `pytest` the test file gets
shorter: neither `main` nor `try` is needed, because `pytest` finds and runs
every function whose name starts with `test_`:

```python
from calculator import square


def test_square():
    assert square(2) == 4
    assert square(3) == 9
    assert square(-2) == 4
    assert square(-3) == 9
    assert square(0) == 0
```

You run the program with `pytest`, not `python`. With the buggy
`calculator.py` (we shortened the version lines at the top of the output and
the time at the end, which depend on the computer):

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 1 item

test_calculator.py F                                 [100%]

======================== FAILURES =========================
_______________________ test_square _______________________

    def test_square():
        assert square(2) == 4
>       assert square(3) == 9
E       assert 6 == 9
E        +  where 6 = square(3)

test_calculator.py:6: AssertionError
================= short test summary info =================
FAILED test_calculator.py::test_square - assert 6 == 9
========================= 1 failed ========================
```

It reads easily: `F` means a test failed, `>` marks the failing line, and `E`
gives the reason: `assert 6 == 9`, where `6` came from `square(3)`. So
`square(3)` returns 6 instead of 9. Once `+` becomes `*`:

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 1 item

test_calculator.py .                                 [100%]

========================= 1 passed ========================
```

A dot (`.`) means a test passed.

`pytest` leaves a test function at its **first** failing `assert`. To see the
whole problem, it is a good habit to split tests into separate functions:
positive numbers, negative numbers, zero.

```python
from calculator import square


def test_positive():
    assert square(2) == 4
    assert square(3) == 9


def test_negative():
    assert square(-2) == 4
    assert square(-3) == 9


def test_zero():
    assert square(0) == 0
```

With `calculator.py` buggy again:

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 3 items

test_calculator.py FF.                               [100%]

======================== FAILURES =========================
______________________ test_positive ______________________

    def test_positive():
        assert square(2) == 4
>       assert square(3) == 9
E       assert 6 == 9
E        +  where 6 = square(3)

test_calculator.py:6: AssertionError
______________________ test_negative ______________________

    def test_negative():
>       assert square(-2) == 4
E       assert -4 == 4
E        +  where -4 = square(-2)

test_calculator.py:10: AssertionError
================= short test summary info =================
FAILED test_calculator.py::test_positive - assert 6 == 9
FAILED test_calculator.py::test_negative - assert -4 == 4
==================== 2 failed, 1 passed ===================
```

The three tests ran separately: `FF.` says two failed and one passed. The
detail in the negative test is interesting: `-2 + -2` is -4, while the square
is 4. The zero test passed, because both `0 + 0` and `0 * 0` are 0. Catching
a bug takes choosing the right case.

You can also test that a function **raises an error**. `square("cat")` should
raise a `TypeError`; `pytest.raises` asserts that (it needs `import pytest` at
the top of the file):

```python
import pytest

from calculator import square


def test_positive():
    assert square(2) == 4
    assert square(3) == 9


def test_negative():
    assert square(-2) == 4
    assert square(-3) == 9


def test_zero():
    assert square(0) == 0


def test_str():
    with pytest.raises(TypeError):
        square("cat")
```

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 4 items

test_calculator.py ....                              [100%]

========================= 4 passed ========================
```

Which cases to test is up to you. A guiding question: **how could this
function have been written wrongly, and which example would catch that?**

## Testing strings

Remember `hello.py` from the first week:

```python
def main():
    name = input("What's your name? ")
    hello(name)


def hello(to="world"):
    print("hello,", to)


if __name__ == "__main__":
    main()
```

```text
$ python hello.py
What's your name? David
hello, David
```

A test for it:

```python
from hello import hello


def test_hello():
    assert hello("David") == "hello, David"
    assert hello() == "hello, world"
```

```text
$ pytest test_hello.py
=================== test session starts ===================
collected 1 item

test_hello.py F                                      [100%]

======================== FAILURES =========================
_______________________ test_hello ________________________

    def test_hello():
>       assert hello("David") == "hello, David"
E       AssertionError: assert None == 'hello, David'
E        +  where None = hello('David')

test_hello.py:5: AssertionError
------------------ Captured stdout call -------------------
hello, David
================= short test summary info =================
FAILED test_hello.py::test_hello - AssertionError: assert...
========================= 1 failed ========================
```

The program greeted correctly, yet the test failed: `hello` **prints** the
greeting but does not **return** it, so the value of `hello("David")` is
`None`. Printing to the screen is a **side effect**: the function does
something but does not give the result back to its caller (the line it printed
sits under `Captured stdout` in the output). A testable function returns its
result with `return` and leaves the printing to `main`:

```python
def main():
    name = input("What's your name? ")
    print(hello(name))


def hello(to="world"):
    return f"hello, {to}"


if __name__ == "__main__":
    main()
```

```text
$ python hello.py
What's your name? David
hello, David
```

```text
$ pytest test_hello.py
=================== test session starts ===================
collected 1 item

test_hello.py .                                      [100%]

========================= 1 passed ========================
```

This test is better split in two as well: the default value and the argument
separately.

```python
from hello import hello


def test_default():
    assert hello() == "hello, world"


def test_argument():
    assert hello("David") == "hello, David"
```

## Organizing tests into folders

As your program grows, so do the test files. `pytest` can run every test in a
folder with one command. Put the tests in a folder called `test`
(`test/test_hello.py`) and add an empty `__init__.py` file to the folder;
`pytest` needs it to treat the folder as a package. Then give the folder's
name:

```text
$ pytest test
=================== test session starts ===================
collected 2 items

test\test_hello.py ..                                [100%]

========================= 2 passed ========================
```

## How Odyssey checks your tests

In this week's exercises **you write the test file**, and the module under
test (like `calculator.py`) is ready. Odyssey first runs your tests with the
correct module: all of them must pass. Then it runs them again with a few
**deliberately broken** versions of the module: with each broken version,
**at least one** of your tests must fail. The `+` bug above is exactly such a
broken version; a test that only tries `square(2)` misses it. CS50's check50
checks the assignments the same way.

## Summing up

Testing is a normal part of programming. Unit tests show that specific parts
of your code work as expected, whether with test programs you write yourself
or with a library like `pytest`:

- Unit tests, and file and function names starting with `test_`
- `if __name__ == "__main__":`
- `assert` and `AssertionError`
- `pytest`: `F` and `.`, splitting tests, `pytest.raises`
- Side effects: `return` instead of `print`
- Organizing tests into a folder (`__init__.py`)

## This week's problem set

The seven exercises in the **Exercise** tab practise this lecture's topics one
by one. The four in the **Problem Set** tab are CS50's assignment for this
week (Problem Set 5): split four programs from earlier weeks into functions
and write their tests.

| Problem | What it asks | First version |
|---|---|---|
| Testing my twttr | `shorten` and its tests | Week 2 |
| Back to the Bank | `value` and its tests | Week 1 |
| Re-requesting a Vanity Plate | `is_valid` and its tests | Week 2 |
| Refueling | `convert`, `gauge` and their tests | Week 3 |

Each problem has two files: the program itself and the `test_` file. Both are
yours; Odyssey checks your program and your tests separately.

---

*This section is translated and adapted from week 5 of Harvard University's [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) (lecture notes and problem set); examples and exercises were changed, and the problem set is checked by Odyssey, not by CS50's check50. The original and this adaptation are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Harvard does not endorse this adaptation.*
