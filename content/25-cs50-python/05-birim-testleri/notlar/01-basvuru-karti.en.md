Everything from week 5 on one page.

## Names

| What | Rule | Example |
|---|---|---|
| Test file | `test_` + the file under test | `test_calculator.py` |
| Test function | starts with `test_` | `def test_zero():` |
| Test folder | an empty `__init__.py` inside | `test/__init__.py` |

`pytest` does not count a function whose name does not start with `test_`.

## Commands

| Command | What it does |
|---|---|
| `pip install pytest` | installs pytest (on your own computer) |
| `pytest test_calculator.py` | runs the tests in that file |
| `pytest test` | runs every test in the `test` folder |
| `python test_calculator.py` | runs the file like an ordinary program |

## Reading the output

| Mark | Meaning |
|---|---|
| `.` | a test passed |
| `F` | a test failed |
| `>` | the line where the test failed |
| `E` | the reason: `assert 6 == 9` |
| `where 6 = square(3)` | where the value came from |
| `2 failed, 1 passed` | the summary |

## Writing tests

| Code | What it asserts |
|---|---|
| `assert square(3) == 9` | the result is 9 |
| `assert hello() == "hello, world"` | the result with the default argument |
| `with pytest.raises(TypeError):` | the line inside must raise `TypeError` |

```python
import pytest

from calculator import square


def test_zero():
    assert square(0) == 0


def test_str():
    with pytest.raises(TypeError):
        square("cat")
```

## A testable program

```python
def main():
    x = int(input("What's x? "))
    print("x squared is", square(x))


def square(n):
    return n * n


if __name__ == "__main__":
    main()
```

- The function **returns** its result (`return`); printing happens in `main`.
- `if __name__ == "__main__":` keeps `main` from running on import.

## Which cases

For each function, think about: an ordinary value, a value at the edge
(0, an empty string, the smallest and the largest), a negative number,
uppercase and lowercase, invalid input (should it raise an error?). The
question is always the same: **how could this function have been written
wrongly, and which example would catch that?**
