# Working with Databases

In the previous section you wrote data to a file. That is perfectly fine for a
hundred rows. But it stops being enough once you start asking:

- "Give me the students whose grade is above 80."
- "Work out the average grade per city."
- "Update this name, but only on this row."

With a file, each of those means writing a loop by hand. A **database**
answers these questions itself.

In this section you will use `sqlite3`. It ships inside Python — no
installation, no server, no account. The whole database is a single file.

## Connecting

```python
import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()

# ... you do your work ...

connection.commit()
connection.close()
```

There are four steps and the order matters:

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>connect</b><br>open the file</span>
    <span class="arrow">→</span>
    <span class="node"><b>cursor</b><br>the command runner</span>
    <span class="arrow">→</span>
    <span class="node"><b>execute</b><br>an SQL command</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>commit</b><br>write to disk</span>
  </div>
  <figcaption>Without a commit, the changes you made never reach the disk — they all disappear when the program closes.</figcaption>
</figure>

If the file does not exist, `connect` creates it. You can also set up a
temporary database in memory:

```python
connection = sqlite3.connect(":memory:")
```

That is ideal for experiments: it disappears when the program ends and leaves
nothing on disk.

## Creating a table

Data in a database lives in **tables**. A table is a structure whose columns
and column types are fixed:

```python
cursor.execute("""
    CREATE TABLE students (
        name TEXT,
        grade INTEGER,
        city TEXT
    )
""")
```

The types you will use:

| SQL type | Python equivalent |
|---|---|
| `TEXT` | `str` |
| `INTEGER` | `int` |
| `REAL` | `float` |
| `NULL` | `None` |

If the table already exists the command raises an error. To avoid that:

```python
cursor.execute("CREATE TABLE IF NOT EXISTS students (name TEXT, grade INTEGER)")
```

## Inserting data

```python
cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", 90))
```

The question marks are **placeholders**. You supply the values as a tuple in
the second argument.

To insert several rows at once, use `executemany`:

```python
rows = [("Ada", 90), ("Brian", 40), ("Grace", 75)]
cursor.executemany("INSERT INTO students VALUES (?, ?)", rows)
```

## Why do the question marks matter?

You could write the value straight into the command, but **nobody does**:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h5>EMBEDDED IN THE STRING — DANGEROUS</h5>
<pre><code>cursor.execute(
    "INSERT INTO students VALUES ('" + name + "', 90)"
)</code></pre>
    </div>
    <div class="ok">
      <h5>PLACEHOLDER — CORRECT</h5>
<pre><code>cursor.execute(
    "INSERT INTO students VALUES (?, ?)",
    (name, 90)
)</code></pre>
    </div>
  </div>
  <figcaption>In the left-hand version a quote inside <code>name</code> breaks the command; a deliberately written string can change the command's meaning entirely. This is called SQL injection.</figcaption>
</figure>

A concrete example: let `name` be `O'Brien`. In the left-hand version the
quote in the middle splits the command in two and you get a
`sqlite3.OperationalError`. In the right-hand version there is no problem at
all — the library places the value safely.

**Rule: values are never pasted into SQL text; they are always supplied with
`?`.**

## Reading data

```python
cursor.execute("SELECT name, grade FROM students")
rows = cursor.fetchall()

print(rows)
```

```
[('Ada', 90), ('Brian', 40), ('Grace', 75)]
```

Each row comes back as a **tuple**. If you want a single row:

```python
cursor.execute("SELECT name FROM students WHERE grade > 80")
row = cursor.fetchone()

print(row)
```

```
('Ada',)
```

When there is no result, `fetchone` returns `None` — you have to check for it.

Note: `fetchall` works once. Call it a second time and you get an empty list,
just like reading a file twice.

## Filtering and sorting

```python
cursor.execute("""
    SELECT name, grade FROM students
    WHERE grade >= 50
    ORDER BY grade DESC
""")

print(cursor.fetchall())
```

```
[('Ada', 90), ('Grace', 75)]
```

- `WHERE` sets a condition — like an `if` in Python.
- `ORDER BY` sorts; `DESC` is largest first, `ASC` (the default) smallest
  first.

Placeholders are used in conditions too:

```python
cursor.execute("SELECT name FROM students WHERE city = ?", ("London",))
```

The comma in a one-element tuple is essential: `("London",)`. Without it that
is not a tuple, just a string in brackets, and you get an error.

## Letting the database do the arithmetic

This is where a database really pays off. Without writing a loop in Python:

```python
cursor.execute("SELECT COUNT(*) FROM students")
print(cursor.fetchone()[0])

cursor.execute("SELECT AVG(grade) FROM students")
print(cursor.fetchone()[0])

cursor.execute("""
    SELECT city, AVG(grade) FROM students
    GROUP BY city
""")
print(cursor.fetchall())
```

`GROUP BY` groups by city and works out the average separately for each group.
Writing that in Python would take ten lines.

| Function | What it does |
|---|---|
| `COUNT(*)` | The number of rows |
| `SUM(column)` | The total |
| `AVG(column)` | The average |
| `MIN` / `MAX` | The smallest / largest |

## Updating and deleting

```python
cursor.execute("UPDATE students SET grade = ? WHERE name = ?", (95, "Ada"))
cursor.execute("DELETE FROM students WHERE grade < ?", (50,))
connection.commit()
```

**Do not forget the `WHERE`.** Without it, `UPDATE` changes every row and
`DELETE` empties the whole table. There is no undo.

## Forgetting to commit

This is the most common mistake:

```python
cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", 90))
connection.close()
```

The program runs, no error. But when you open the file later, Ada is not
there.

The reason: the database keeps changes inside a **transaction** and does not
make them permanent until `commit` is called. When `close` is called, an
uncommitted transaction is rolled back.

Read commands (`SELECT`) need no commit; only commands that change something
do.

## Summary

- `sqlite3` ships inside Python; it needs no server, no installation and no
  account.
- The order is `connect` → `cursor` → `execute` → `commit` → `close`.
- Data lives in **tables**; a table is created with `CREATE TABLE`.
- Values are never **pasted** into SQL text; they are supplied with the `?`
  placeholder.
- `SELECT` reads, `fetchall` gives every row and `fetchone` gives a single
  row.
- `WHERE` filters, `ORDER BY` sorts, `GROUP BY` groups.
- `COUNT`, `SUM`, `AVG`, `MIN` and `MAX` let the database do the arithmetic.
- Forgetting `WHERE` in `UPDATE` or `DELETE` affects the entire table.
- Without a `commit`, your changes are lost.
