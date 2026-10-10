## unittest

| Code | What it does |
|---|---|
| `class TestX(unittest.TestCase):` | a test class |
| `def test_...(self):` | one test |
| `def setUp(self):` / `tearDown` | before / after every test |
| `unittest.main()` | run the tests in the file |
| `python -m unittest` | find and run the `test_*.py` files in the folder |

## assert methods

| Code | Fails when |
|---|---|
| `assertEqual(a, b)` | `a != b` |
| `assertTrue(x)` / `assertFalse(x)` | `x` is false / true |
| `assertIn(a, b)` | `a` is not in `b` |
| `assertIsNone(x)` | `x` is not `None` |
| `assertAlmostEqual(a, b)` | they differ at 7 decimal places |
| `with assertRaises(Error):` | that error did not happen in the block |
| `with subTest(x=x):` | a separate report for each value in a loop |

## unittest.mock

| Code | What it does |
|---|---|
| `@patch("module.name", return_value=10)` | replace the name with a fake during the test |
| `with patch("module.name") as fake:` | the same with a block |
| `fake.side_effect = ValueError("x")` | raise when called |
| `fake.call_count` | how many times it was called |
| `fake.assert_called_once_with(...)` | once, with these arguments? |

## doctest

| Code | What it does |
|---|---|
| `>>> expression` + the result on the next line | an example in a docstring |
| `doctest.testmod()` | try the examples in the file; `TestResults(failed, attempted)` |
| `python -m doctest file.py -v` | from the command line |
