**Running**

| Command | What it does |
|---|---|
| `python -m pytest` | Finds and runs all the tests in the folder. |
| `python -m pytest -q` | Short output: one dot per test, a summary at the end. |
| `python -m pytest -v` | Each test on its own line, with its name. |
| `python -m pytest -x` | Stops at the first failing test. |
| `python -m pytest -k discount` | Only the tests with `discount` in their name. |
| `python -m pytest test_cart.py` | Only this file. |
| `python -m pytest --tb=short` | A short error report. |

Writing `python -m pytest` instead of `pytest` makes it clear which Python
runs the tests, and it adds the project folder to the import path.

**What pytest counts as a test**

- Files whose names start with `test_` or end with `_test.py`.
- In those files, functions whose names start with `test_`.
- The `test_` methods of classes whose names start with `Test`.

**Exit codes**

| Code | Meaning | In the pipeline |
|---|---|---|
| `0` | All tests passed | Green |
| `1` | At least one test failed | Red |
| `2` | The user interrupted it | Red |
| `5` | No tests were found | Red |

**Patterns**

```python
assert result == expected

with pytest.raises(ValueError):
    bad_call()

@pytest.mark.parametrize("value, expected", [(1, 2), (3, 4)])
def test_example(value, expected):
    assert operation(value) == expected
```
