In this exercise you will put the database work inside functions — that is
how code is organised in a real program.

The connection and the table are ready for you. You will write three
functions; all of them use the `cursor` and `connection` variables.

**What you need to do:**

1. `add_student(name, grade)` — inserts a row, calls `commit` and returns the
   **total number of rows** in the table.

2. `update_grade(name, grade)` — updates that name's grade, calls `commit` and
   returns the **number of affected rows** (`cursor.rowcount`).
   If there is no such name it must return `0`.

3. `find_grade(name)` — returns that name's grade. If the name is not there it
   returns `None`.

4. Do the following in order and print each result:
   - `add_student("Ada", 90)`
   - `add_student("Brian", 40)`
   - `update_grade("Ada", 95)`
   - `find_grade("Ada")`
   - `find_grade("Nobody")`

**Expected output:**

```
1
2
1
95
None
```

Note: for `find_grade` you have to **check** the result of `fetchone`; when
there is no result it is `None`, and writing `[0]` raises an error.

> Always supply values with `?`. Do not forget `UPDATE ... WHERE name = ?` —
> without the `WHERE` the whole table is updated.
