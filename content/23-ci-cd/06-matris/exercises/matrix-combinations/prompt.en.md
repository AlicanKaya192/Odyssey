Write the function `combinations(matrix)`. It should return all combinations of the matrix in a list, each one a dictionary. Do not use `itertools`.

The order is like GitHub's: the first key is the outermost. For `{"os": [A, B], "python": [X, Y]}`:

- `{"os": A, "python": X}`, `{"os": A, "python": Y}`, `{"os": B, "python": X}`, `{"os": B, "python": Y}`

The idea: start with `[{}]` (a single, empty combination). For each key, extend every combination you have with every value of that key.

**Expected output:**

```
{'os': 'ubuntu-latest', 'python': '3.12'}
{'os': 'ubuntu-latest', 'python': '3.13'}
{'os': 'windows-latest', 'python': '3.12'}
{'os': 'windows-latest', 'python': '3.13'}
12
```
