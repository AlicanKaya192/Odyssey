| Symptom | Cause | Fix |
|---|---|---|
| `no tests ran`, exit code `5` | The file or function name does not start with `test_`. | `test_cart.py`, `def test_...`. |
| `ModuleNotFoundError: No module named 'cart'` | The tests are run from outside the project folder. | `python -m pytest` in the project folder. |
| The test always passes, even when the code is broken | There is no `assert`, or it checks something that is always true (`assert cart_total`). | Compare the result with a value; break the code and see the test fail. |
| `assert 0.30000000000000004 == 0.3` | Decimal numbers cannot be stored exactly in a computer. | `assert x == pytest.approx(0.3)` or `round`. |
| Tests pass one by one but fail together | One test depends on the state (a file, a list) another one left behind. | Let every test prepare its own data. |
| A `pytest.raises` test fails: `DID NOT RAISE` | The code does not raise the expected error. | Fix the code; or the error type is written wrong. |
| Passes for me, fails in the pipeline | A package is missing in the pipeline or the Python version is different. | `requirements.txt` and `python-version`. |

**Rule:** before fixing a bug, write the test that catches it. The test
should fail first and pass after the fix; if the bug ever comes back, the
pipeline catches it.
