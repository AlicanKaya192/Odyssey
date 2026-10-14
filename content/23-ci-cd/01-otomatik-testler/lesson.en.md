# Automated Tests

In the previous section we saw that the pipeline tests the code on every
change. But the pipeline does not **write** the tests; it only runs them.
For a team that writes no tests, CI only tells you that the code can be
installed; it cannot tell you that it works. In this section we write
tests with **pytest**, the most common test tool in Python, read a failing
test and see how the pipeline decides between "passed" and "failed".

## Why trying it by hand is not enough

Imagine you wrote a function that adds up the total of a shopping cart.
After writing it you call it a few times and look at the result; if it is
right, you move on. That is a test, but a test done **by hand**:

- A week later, when you change the function, you forget to try the same
  things again.
- When someone else changes the function, they do not know which cases you
  tried.
- Five tries for each of ten functions means fifty tries on every change.

An **automated test** means writing that try down as code once: a small
function that calls your function and **checks** that the result is the
expected value. It is written once and runs again as often as you like, in
seconds. That is exactly what the pipeline does: it runs all the tests on
every change.

## The code under test

Let us take a cart total as the example. The discount is given as a
percentage:

```python
def cart_total(prices, discount=0):
    total = sum(prices)
    if discount:
        total = total - total * discount / 100
    return round(total, 2)
```

This code lives in a file called `cart.py`.

## The first tests

The shortest way to check that something is true in Python is the
`assert` statement: you write `assert condition`; if the condition is true
nothing happens, if it is false the program stops with an
`AssertionError`.

pytest is built on top of this statement. Its rules are simple:

- The name of the test file starts with `test_`: `test_cart.py`.
- Each test inside it is a function, and its name starts with `test_` too.
- Inside the function you call the code under test and check the result
  with `assert`.

`test_cart.py`:

```python
from cart import cart_total


def test_total_without_discount():
    assert cart_total([10, 20, 30]) == 60


def test_total_with_discount():
    assert cart_total([50, 50], discount=20) == 80


def test_empty_cart():
    assert cart_total([]) == 0
```

Each test's name says what it tries. When a test fails, its name is the
first thing you see; a name like `test_1` tells you nothing there.

To run the tests, type this in the terminal, in the project folder:

```text
python -m pytest -q
```

pytest finds the files whose names start with `test_` by itself and runs
the `test_` functions in them. `-q` (quiet) keeps the output short. The
result:

```text
...                                                                      [100%]
3 passed
```

Each dot (`.`) is a passing test. The last line is the summary. The time
changes on every run, so we removed it from the outputs.

## How to read a failing test

Now someone makes a small typo in `cart.py`: `10` instead of `100`.

```python
def cart_total(prices, discount=0):
    total = sum(prices)
    if discount:
        total = total - total * discount / 10
    return round(total, 2)
```

The tests did not change. Running them again (`--tb=short` keeps the
error report short):

```text
.F.                                                                      [100%]
================================== FAILURES ===================================
__________________________ test_total_with_discount ___________________________
test_cart.py:9: in test_total_with_discount
    assert cart_total([50, 50], discount=20) == 80
E   assert -100.0 == 80
E    +  where -100.0 = cart_total([50, 50], discount=20)
=========================== short test summary info ===========================
FAILED test_cart.py::test_total_with_discount - assert -100.0 == 80
1 failed, 2 passed
```

Read it in this order:

1. **The dots and the `F`:** the second test failed (`F`, failed), the
   other two passed.
2. **Which test:** `test_total_with_discount`. Thanks to its name we know
   the problem is in the discount before even looking at the code.
3. **Which line and why:** `assert -100.0 == 80`. The function should
   have returned `80`; it returned `-100.0`.
4. **The summary:** `1 failed, 2 passed`.

The tests without a discount still pass, because the mistake is only in
the discount branch. That is why testing each case in its own test helps:
the name of the failing test shows where the problem is.

## The exit code: how the pipeline decides

The pipeline does not read the output of a test; it looks at the
command's **exit code**. Every program leaves a number to the operating
system when it ends: `0` means "all fine", any number other than `0` means
"something went wrong". The step `run: python -m pytest` in a workflow
fails if the exit code is not `0`, and the pipeline stops there.

pytest's exit codes, measured by running the same tests in three
situations:

```text
all tests pass  -> exit code 0
one test fails  -> exit code 1
no test files   -> exit code 5
```

- `0`: all tests passed → the step is green.
- `1`: at least one test failed → the step is red.
- `5`: no tests were found → the step is red too. Forgetting to start a
  file name with `test_` makes the tests silently disappear; pytest
  counts that as an error, and it is good that it does.

## Expecting an error: `pytest.raises`

Sometimes the right behaviour is to raise an error. A 150 percent discount
makes no sense; instead of quietly calculating it, the function should
reject it:

```python
def cart_total(prices, discount=0):
    if discount < 0 or discount > 100:
        raise ValueError("discount must be between 0 and 100")
    total = sum(prices)
    if discount:
        total = total - total * discount / 100
    return round(total, 2)
```

We check that the error is really raised with `pytest.raises`. If the code
inside the `with` block does not raise an error of that kind, the test
fails:

```python
import pytest

from cart import cart_total


def test_discount_over_100_is_rejected():
    with pytest.raises(ValueError):
        cart_total([10], discount=150)


def test_negative_discount_is_rejected():
    with pytest.raises(ValueError):
        cart_total([10], discount=-5)
```

```text
..                                                                       [100%]
2 passed
```

## The same test with many inputs: `parametrize`

You do not need five functions to make the same check with five
different inputs. `@pytest.mark.parametrize` runs one test function
separately with each row of inputs you give:

```python
import pytest

from cart import cart_total


@pytest.mark.parametrize("prices, discount, expected", [
    ([10, 20], 0, 30),
    ([100], 25, 75),
    ([19.99, 0.01], 50, 10),
    ([], 30, 0),
])
def test_cart_total(prices, discount, expected):
    assert cart_total(prices, discount) == expected
```

The names in the first text (`prices, discount, expected`) are given the
three values of each row in order. `-v` (verbose) shows each test on its
own line:

```text
============================= test session starts =============================
collecting ... collected 4 items

test_param.py::test_cart_total[prices0-0-30] PASSED                      [ 25%]
test_param.py::test_cart_total[prices1-25-75] PASSED                     [ 50%]
test_param.py::test_cart_total[prices2-50-10] PASSED                     [ 75%]
test_param.py::test_cart_total[prices3-30-0] PASSED                      [100%]

============================== 4 passed ==============================
```

Four rows, four separate tests. If one fails, the input it failed on is
written inside the square brackets.

## What makes a good test

- **One behaviour.** A test tries one thing, and its name says what.
- **Arrange, act, assert.** Prepare the input, call the code, check the
  result with `assert`. Keep all three short.
- **Try the edges.** An empty list, zero, the largest value, bad input.
  Mistakes often hide at the edges: like the difference between `<` and
  `<=`.
- **See the test fail.** Break the code on purpose and see the test fail.
  A test that never fails protects nothing.
- **Independent and fast.** Tests should not depend on each other's
  results, and they should give the same result in any order. The
  pipeline will run all of them on every change.

## Tests in the pipeline

The workflow file from the previous section now makes more sense: the
`pytest` package is listed in `requirements.txt`, the install step
installs it, the last step runs the tests, and the pipeline turns green or
red depending on the exit code.

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

`on: [push, pull_request]` means run on both events: when code is pushed
and when someone opens a pull request. We look at triggers in detail in
the fourth section.

## This section's exercises

In the test exercises you write the tests in `main.py`; the module under
test is in the other tab, read-only. Odyssey first runs your tests on the
correct code (all of them must pass), then on versions of the code that
were **broken on purpose** (on each of them at least one test must fail).
A set of tests that cannot catch a broken version is incomplete; the
message tells you which mistake it missed.

## Summary

- An automated test writes a try down as code once; the pipeline runs it
  on every change.
- pytest finds the files and functions that start with `test_`; checks are
  made with `assert`.
- A failing test: its name, its line and the two values in the `assert`
  line show the problem.
- The pipeline decides from the exit code: `0` green, `1` failed, `5` no
  tests.
- `pytest.raises` tries an expected error; `parametrize` tries the same
  test with many inputs.
