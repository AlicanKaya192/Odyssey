In a real project the tests live next to the code in a separate **`tests`**
folder, and one command runs them all. The code below builds a small project
and runs its tests by **discovering** them:

```python
import io
import unittest
from pathlib import Path

Path("shop").mkdir()
Path("shop/__init__.py").write_text("")
Path("shop/prices.py").write_text(
    "def with_tax(price, rate=0.2):\n"
    "    return round(price * (1 + rate), 2)\n")
Path("tests").mkdir()
Path("tests/__init__.py").write_text("")
Path("tests/test_prices.py").write_text(
    "import unittest\n"
    "from shop.prices import with_tax\n\n\n"
    "class TestWithTax(unittest.TestCase):\n"
    "    def test_default(self):\n"
    "        self.assertEqual(with_tax(10), 12.0)\n\n"
    "    def test_zero_rate(self):\n"
    "        self.assertEqual(with_tax(10, 0), 10)\n")
suite = unittest.defaultTestLoader.discover("tests", top_level_dir=".")
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
print(result.testsRun, result.wasSuccessful())
```

```text
2 True
```

## Folder layout

```text
project/
  shop/
    __init__.py
    prices.py
  tests/
    __init__.py
    test_prices.py
```

- Test file names start with **`test_`**; discovery looks for these names.
- From the project folder on the command line: `python -m unittest` (or
  `python -m unittest discover -s tests`). `pytest` finds the same folder by
  itself.
- Tests check the code by **importing** it (`from shop.prices import
  with_tax`); they do not copy it.

## A good test

- **Arrange – act – assert:** set up the input, call the function once, check
  the result. One test checks one behaviour.
- **Its name says what it checks:** `test_zero_rate`, `test_empty_list`; when
  it fails, the report tells what broke.
- **Edge cases:** empty input, a single item, zero, negative, a very large
  value, the wrong type, an expected error (`assertRaises`).
- **Independent and repeatable:** order does not matter; the network, the
  clock and randomness are pinned with fake objects or a fixed seed.
- **Fast:** tests finish in seconds so they are run often.
- When a bug is found, first write the test that catches it, then fix it: the
  same bug never comes back.
