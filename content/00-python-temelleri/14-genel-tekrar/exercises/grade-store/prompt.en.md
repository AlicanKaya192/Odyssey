The last exercise: a database, error handling and type annotations together.

The connection and the table are ready for you.

**What you need to do:**

1. The `save(name, raw)` function — annotated `(str, str) -> bool`:
   - Try to turn the `raw` string into a number.
   - If it converts, insert the row, call `commit` and return `True`.
   - If it does not (`ValueError`), insert **nothing** and return `False`.

2. The `find(name)` function — annotated `(str) -> int | None`:
   - Returns that name's grade, or `None` if the name is not there.

3. The `average()` function — annotated `() -> int`:
   - Returns the average of the grades **rounded to a whole number**.
   - Returns `0` when the table is empty. (`AVG` gives `None` on an empty
     table.)

4. Save these values in order and print each result:
   `("Ada", "90")`, `("Brian", "oops")`, `("Grace", "76")`

5. Then print these in order: `find("Ada")`, `find("Nobody")`, `average()`

**Expected output:**

```
True
False
True
90
None
83
```

The average: `(90 + 76) / 2 = 83.0`. Brian was never saved.

> `AVG` returns `None` on an empty table, so you have to check for that inside
> `average`.
