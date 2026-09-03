Database mistakes fall into two groups: those that raise an error at once, and
those that quietly lose data. The second group is the dangerous one.

## 1. Forgetting to commit

```python
cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", 90))
connection.close()
```

The program runs without error. But when you open the file later, Ada is not
there.

A database keeps changes inside a **transaction** and does not make them
permanent until `commit` is called. When `close` is called, an uncommitted
transaction is rolled back.

`SELECT` does not need it; only `INSERT`, `UPDATE`, `DELETE` and `CREATE` do.

The way not to forget is to use `with`:

```python
with sqlite3.connect("school.db") as connection:
    cursor = connection.cursor()
    cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", 90))
```

If the block finishes without an error, `commit` is called for you; if an
error comes up, the changes are rolled back.

**But watch out:** unlike `with` on files, this does **not close the
connection.** You still have to close it yourself.

## 2. Pasting a value into the command

```python
name = "O'Brien"
cursor.execute("INSERT INTO students VALUES ('" + name + "', 90)")
```

```
sqlite3.OperationalError: near "Brien": syntax error
```

The quote in the middle splits the command in two. That is what happens with a
well-meaning user's name.

A deliberately written string can change the command's meaning — this is
called **SQL injection**, and it is one of the oldest vulnerabilities in
software security.

The fix is always the same:

```python
cursor.execute("INSERT INTO students VALUES (?, ?)", (name, 90))
```

When you use a placeholder, the library places the value as **data**, not as
part of the command. That is exactly the difference between the two.

## 3. Forgetting the comma in a one-element tuple

```python
cursor.execute("SELECT name FROM students WHERE city = ?", ("London"))
```

```
ValueError: parameters are of unsupported type
```

`("London")` is not a tuple — it is a string in brackets. In Python a tuple is
made by the comma:

```python
cursor.execute("SELECT name FROM students WHERE city = ?", ("London",))
```

The trailing comma looks odd but it is necessary. A list works too:

```python
cursor.execute("SELECT name FROM students WHERE city = ?", ["London"])
```

## 4. Forgetting the `WHERE`

```python
cursor.execute("UPDATE students SET grade = 0")
cursor.execute("DELETE FROM students")
```

Both run without error. The first sets every grade to zero; the second empties
the table. There is no undo.

A habit worth building: when writing a delete or an update, write the `WHERE`
part first and the beginning afterwards.

There is also a way to check — look with a `SELECT` first:

```python
cursor.execute("SELECT COUNT(*) FROM students WHERE grade < 50")
print(cursor.fetchone()[0])       # how many rows will this affect?
```

## 5. Reading again after `fetchall`

```python
cursor.execute("SELECT name FROM students")
first = cursor.fetchall()
second = cursor.fetchall()

print(len(first), len(second))
```

```
3 0
```

A result set is read once, just like the read position in a file. The second
`fetchall` gives an empty list.

The fix: read once, keep it in a variable.

## 6. Not checking the result of `fetchone`

```python
cursor.execute("SELECT name FROM students WHERE grade > 200")
row = cursor.fetchone()

print(row[0])
```

```
TypeError: 'NoneType' object is not subscriptable
```

When there is no result, `fetchone` returns `None`. You have to check:

```python
row = cursor.fetchone()
if row is None:
    print("not found")
else:
    print(row[0])
```

In the language of type annotations: the return of `fetchone` is
`tuple | None`.

## 7. Forgetting that a row is a tuple

```python
cursor.execute("SELECT COUNT(*) FROM students")
print(cursor.fetchone())
```

```
(3,)
```

You expected `3` and got `(3,)`. Even when you ask for a single column, the
row comes back as a tuple. You need an index to get the value:

```python
print(cursor.fetchone()[0])
```

```
3
```

## 8. SQLite is relaxed about types

```python
cursor.execute("CREATE TABLE students (name TEXT, grade INTEGER)")
cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", "not a number"))
connection.commit()
```

No error. SQLite treats a column type as a **suggestion** and accepts values
that do not match. Most other databases reject them.

What that means: validating the data is left **to you**. Guarding an `int()`
conversion with `try` / `except` earns its keep here.

## 9. Not closing the connection

```python
connection = sqlite3.connect("school.db")
# ... work done, but close was never called
```

In small scripts this usually causes no trouble; the operating system cleans
up when the program ends. But while the file stays open it counts as locked,
and another process trying to write gets a `database is locked` error.

In a long-running program, a leaked connection is a real problem.

## Summary

| Trap | What happens |
|---|---|
| Forgetting `commit` | The changes are lost |
| Embedding a value in the text | An error, or SQL injection |
| Forgetting the comma in a tuple | `unsupported type` |
| Forgetting the `WHERE` | The whole table is affected |
| Calling `fetchall` twice | The second one is empty |
| Not checking `fetchone` | A `NoneType` error |
| Forgetting the tuple | `(3,)` where you expected `3` |
| Trusting the column type | A wrong type slips in silently |
| Not closing the connection | `database is locked` |
