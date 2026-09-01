Instead of inserting rows one at a time, you will insert them all at once.

**What you need to do:**

1. Connect to the `":memory:"` database and create the `students` table:
   `name TEXT`, `grade INTEGER`, `city TEXT`.
2. Insert these rows **with `executemany`**:

```python
[
    ("Ada", 90, "London"),
    ("Brian", 40, "London"),
    ("Grace", 75, "New York"),
    ("Alan", 60, "London"),
]
```

3. Make the changes permanent.
4. Hold the total number of rows in a variable called `total` (use
   `COUNT(*)`).
5. Hold every name as a **list** in a variable called `names`. Since each row
   comes back as a tuple, you have to pull the names out one by one.
6. Print `total` first, then `names`.

**Expected output:**

```
4
['Ada', 'Brian', 'Grace', 'Alan']
```

> The `COUNT(*)` result also arrives as a row: `cursor.fetchone()[0]`
