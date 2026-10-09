Write the context manager `transaction(data)` with `@contextmanager`: on
entry take a copy of the dictionary and give `data` (`yield data`). If an
error occurs in the block, restore the dictionary from its copy (`clear` +
`update`) and **raise the error again** (`raise`).

**Expected output:**

```
{'balance': 70}
ValueError: not enough money
{'balance': 70}
```
