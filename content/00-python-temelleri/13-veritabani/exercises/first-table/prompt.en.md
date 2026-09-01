You are going to set up your first database. To leave nothing on disk, you
will work in memory.

**What you need to do:**

1. Import the `sqlite3` module and connect to the `":memory:"` database. Hold
   the connection in a variable called `connection`.
2. Get a `cursor`.
3. Create a table called `students` with `name TEXT` and `grade INTEGER`.
4. Insert two rows: `("Ada", 90)` and `("Brian", 40)`. Supply the values with
   the `?` placeholder.
5. Make the changes permanent.
6. Read every row, hold it in a variable called `rows` and print it.
7. Print the number of rows.

**Expected output:**

```
[('Ada', 90), ('Brian', 40)]
2
```

Note: each row comes back as a **tuple**, not a dictionary.

> The insert command is
> `cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", 90))`
