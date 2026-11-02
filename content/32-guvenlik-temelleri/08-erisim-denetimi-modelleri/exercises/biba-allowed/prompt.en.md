The Biba model protects integrity. Levels from low to high:
`LEVELS = ["low", "medium", "high"]`.

`biba_allowed(subject, obj, action)` should return:

- `"read"`: `True` if the subject's level is **equal to or lower** than the
  object's (no read down),
- `"write"`: `True` if the subject's level is **equal to or higher** than
  the object's (no write up),
- any other action: `False`.

The starter code is Bell-LaPadula; Biba is its opposite.

**Expected output:**

```
medium low False True
medium high True False
high high True True
False
```
