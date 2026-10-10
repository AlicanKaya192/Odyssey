# unittest and doctest

You wrote a function, tried it with a few values, it works. A month later you
make a small change; how will you know the old cases still work? Trying again
by hand gets forgotten. A **test** turns the expectation "this input must give
that result" into code, and it runs again in seconds every time. This section
covers two tools in the standard library: **`unittest`** (test classes, fake
objects) and **`doctest`** (examples inside documentation). The `pytest`
covered in the Writing APIs module can run these tests too.

## Your first test class

```python
import io
import unittest


def word_count(text):
    return len(text.split())


class TestWordCount(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(word_count("a b c"), 3)

    def test_empty(self):
        self.assertEqual(word_count(""), 0)

    def test_spaces(self):
        self.assertEqual(word_count("  a   b "), 2)


suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestWordCount)
stream = io.StringIO()
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
for line in stream.getvalue().splitlines():
    if line.endswith("ok"):
        print(line)
print(result.testsRun, result.wasSuccessful())
```

```text
test_empty (__main__.TestWordCount.test_empty) ... ok
test_simple (__main__.TestWordCount.test_simple) ... ok
test_spaces (__main__.TestWordCount.test_spaces) ... ok
3 True
```

- Tests are gathered in a class derived from **`unittest.TestCase`**. Every
  method whose name starts with **`test_`** is a separate test.
- **`self.assertEqual(actual, expected)`** fails the test if the two are not
  equal.
- At the end of a real test file you write `unittest.main()`, or run
  `python -m unittest` on the command line. Here we set up the runner by hand
  so the output can be put on the page, and skipped the timing line.
- Each test runs independently; one failing does not stop the others.

## What does a failing test say?

```python
import io
import unittest


def average(values):
    return sum(values) // len(values)


class TestAverage(unittest.TestCase):
    def test_whole(self):
        self.assertEqual(average([2, 4]), 3)

    def test_fraction(self):
        self.assertEqual(average([1, 2]), 1.5)


suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAverage)
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
print(result.testsRun, len(result.failures))
name, report = result.failures[0]
print(name.id().split(".")[-1])
print(report.strip().splitlines()[-1])
```

```text
2 1
test_fraction
AssertionError: 1 != 1.5
```

- `average` uses `//` (floor division) by mistake. For `[2, 4]` the result is
  still right (3); the bug only shows with an average that has a fraction.
  **A single "happy path" test would have missed this bug**; tests must cover
  edge cases too.
- The report of the failing test says which test failed and what was
  expected: `1 != 1.5` (actual ≠ expected).

## More asserts, setUp and subTest

```python
import io
import unittest


class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("not enough money")
        self.balance -= amount


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(100)

    def test_withdraw(self):
        self.account.withdraw(30)
        self.assertEqual(self.account.balance, 70)

    def test_too_much(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(500)
        self.assertEqual(self.account.balance, 100)

    def test_many(self):
        for amount in [0, 1, 100]:
            with self.subTest(amount=amount):
                Account(100).withdraw(amount)

    def test_float(self):
        self.assertAlmostEqual(0.1 + 0.2, 0.3)


suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAccount)
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
print(result.testsRun, result.wasSuccessful())
```

```text
4 True
```

- **`setUp`** runs **before** every test: each test starts with a clean
  account. (`tearDown` runs after every test; for deleting files, closing
  connections.)
- **`with self.assertRaises(ValueError):`** expects this error in the block;
  if it does not come, the test fails. We also checked that the balance did
  not change after the error.
- **`subTest`** makes each value in a loop a separate sub-test; if one fails,
  the report says which value it failed on.
- **`assertAlmostEqual`** compares floats while tolerating a tiny difference
  (the decimal section).
- Common ones: `assertTrue`, `assertFalse`, `assertIn`, `assertIsNone`,
  `assertIsInstance`, `assertGreater`.

## Fake objects: unittest.mock

```python
import io
import unittest
from unittest.mock import patch


def fetch_price(symbol):
    raise ConnectionError("no network in tests")


def portfolio_value(holdings):
    return sum(qty * fetch_price(symbol) for symbol, qty in holdings.items())


class TestPortfolio(unittest.TestCase):
    @patch("__main__.fetch_price", return_value=10)
    def test_value(self, fake):
        self.assertEqual(portfolio_value({"AAA": 3, "BBB": 2}), 50)
        self.assertEqual(fake.call_count, 2)
        fake.assert_any_call("AAA")


suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPortfolio)
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
print(result.testsRun, result.wasSuccessful())
```

```text
1 True
```

- The real `fetch_price` goes to the network (here it cannot, so it raises).
  A test must not depend on the network, the clock or randomness: it must
  give the same result on every run.
- **`@patch("module.name", return_value=10)`** replaces that name with a fake
  object (a Mock) for the duration of the test; when the test ends, the old
  one comes back. Here the module is `__main__`; in a real project you write
  the name **where it is used**, like `"shop.prices.fetch_price"`.
- The fake object remembers how many times and with what it was called:
  `call_count`, `assert_any_call`, `assert_called_once_with`.

## doctest: examples in the documentation

```python
import contextlib
import doctest
import io


def slugify(title):
    """Turn a title into a piece of a web address.

    >>> slugify("Hello World")
    'hello-world'
    >>> slugify("  Many   spaces  ")
    'many-spaces'
    >>> slugify("")
    ''
    """
    return "-".join(title.lower().split())


def broken_double(x):
    """
    >>> broken_double(2)
    4
    """
    return x + 2 + 1


print(doctest.run_docstring_examples(slugify, globals()))
with contextlib.redirect_stdout(io.StringIO()) as report:
    results = doctest.testmod()
print(results)
lines = report.getvalue().splitlines()
start = lines.index("Expected:")
print(lines[start:start + 4])
```

```text
None
TestResults(failed=1, attempted=4)
['Expected:', '    4', 'Got:', '    5']
```

- The **`>>>`** lines inside a docstring are examples; the line below each is
  the expected output. **`doctest`** runs these examples and compares.
- Since all three of `slugify`'s examples match, `run_docstring_examples`
  printed nothing (`None`).
- `testmod()` tries every docstring in the file: 4 examples, 1 failed. It
  normally prints the failing example's report to the screen; here we caught
  it with `redirect_stdout` and showed only the expected / got part:
  `broken_double(2)` gave `5` instead of `4`.
- Doctest keeps documentation **correct**: if an example goes stale, the test
  fails. On its own it is not enough for logic with many edge cases; it is
  used together with `unittest`/`pytest`.

## unittest or pytest?

| | `unittest` | `pytest` |
|---|---|---|
| Installing | standard library | a package (`pip install pytest`) |
| Writing | a class + `self.assertEqual` | a plain function + `assert` |
| Running | `python -m unittest` | `pytest` (also runs unittest tests) |
| Fake objects | `unittest.mock` | `unittest.mock` or `monkeypatch` |

Both carry the same idea. Use whichever your team uses; `pytest` is common in
new projects, but `unittest` is ready in every Python installation.

## Summary

- `unittest.TestCase` + methods starting with `test_`; `assertEqual`,
  `assertRaises`, `assertAlmostEqual`.
- `setUp` before every test; `subTest` for values in a loop.
- Tests cover edge cases: empty, single item, fractional, bad input.
- `unittest.mock.patch` replaces outside things like the network or the clock
  during a test.
- `doctest` runs the `>>>` examples in docstrings.
