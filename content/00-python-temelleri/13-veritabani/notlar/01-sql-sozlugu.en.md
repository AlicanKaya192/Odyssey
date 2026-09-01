# SQL Reference

A list of the SQL commands you will use in this section. Look here when you
get stuck.

SQL is not Python — it is a separate language. You tell the database what you
want in SQL, and Python only carries that text.

## Creating a table

```sql
CREATE TABLE students (
    name TEXT,
    grade INTEGER,
    city TEXT
)
```

So that it raises no error when the table exists:

```sql
CREATE TABLE IF NOT EXISTS students (name TEXT, grade INTEGER)
```

### Column constraints

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    grade INTEGER DEFAULT 0
)
```

| Constraint | What it does |
|---|---|
| `PRIMARY KEY` | Identifies the row uniquely |
| `NOT NULL` | Cannot be left empty |
| `DEFAULT x` | Uses `x` when no value is given |
| `UNIQUE` | The same value cannot go in twice |

When you write `INTEGER PRIMARY KEY`, SQLite **fills that column itself** —
giving each new row the next number. That is why you can leave the column out
of an `INSERT`.

## Inserting data

Into every column, in order:

```sql
INSERT INTO students VALUES (?, ?, ?)
```

Into named columns:

```sql
INSERT INTO students (name, grade) VALUES (?, ?)
```

The second form is safer: if a column is added to the table later, the command
does not break.

## Reading

```sql
SELECT name, grade FROM students
SELECT * FROM students
```

`*` means every column. In real code writing them out is preferred — with `*`,
your code breaks silently when the column order changes.

### Filtering

```sql
SELECT name FROM students WHERE grade >= 50
```

| Operator | Meaning |
|---|---|
| `=` | Equal to (a single equals sign, not Python's `==`) |
| `!=` or `<>` | Not equal to |
| `>` `<` `>=` `<=` | Comparison |
| `AND` `OR` `NOT` | Logic (as in Python) |
| `IN (a, b)` | One of these |
| `BETWEEN a AND b` | Within a range |
| `LIKE 'A%'` | A text pattern — `%` is anything |
| `IS NULL` | Is it empty |

Watch out: equality in SQL is a **single equals sign**. If Python habits make
you write `==`, SQLite accepts it but other databases do not.

Checking for emptiness is not done with `= NULL` but with `IS NULL`.

### Sorting and limiting

```sql
SELECT name, grade FROM students
ORDER BY grade DESC
LIMIT 3
```

`LIMIT` says how many rows you want. It is a lifesaver on large tables.

## Letting the database calculate

```sql
SELECT COUNT(*) FROM students
SELECT AVG(grade) FROM students
SELECT MAX(grade), MIN(grade) FROM students
```

### Grouped

```sql
SELECT city, COUNT(*), AVG(grade)
FROM students
GROUP BY city
```

One row comes back per city. To filter the grouped result you use `HAVING`
rather than `WHERE`:

```sql
SELECT city, AVG(grade)
FROM students
GROUP BY city
HAVING AVG(grade) > 70
```

The difference: `WHERE` filters rows **before** grouping, `HAVING` filters
groups **after** it.

## Changing data

```sql
UPDATE students SET grade = ? WHERE name = ?
DELETE FROM students WHERE grade < ?
```

**Without a `WHERE`, both affect the entire table.** There is no undo.

One habit worth picking up: write the delete as a `SELECT` first, see how many
rows come back, then run the `DELETE`.

```sql
SELECT * FROM students WHERE grade < 50      -- look first
DELETE FROM students WHERE grade < 50        -- then delete
```

## The Python side

| Python | What it does |
|---|---|
| `sqlite3.connect(path)` | Connects, creating the file if it is missing |
| `connection.cursor()` | Gives you a command runner |
| `cursor.execute(sql, values)` | Runs a single command |
| `cursor.executemany(sql, rows)` | Runs the same command over many rows |
| `cursor.fetchall()` | Gives every result row as a list |
| `cursor.fetchone()` | Gives a single row, or `None` |
| `cursor.lastrowid` | The `id` of the last inserted row |
| `cursor.rowcount` | How many rows the last command affected |
| `connection.commit()` | Makes the changes permanent |
| `connection.close()` | Closes the connection |

## Getting rows as dictionaries

By default rows come back as tuples and you reach columns by position:

```python
row = cursor.fetchone()
print(row[0])
```

The order is easy to get wrong. Reaching them by name is safer:

```python
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("SELECT name, grade FROM students")
row = cursor.fetchone()

print(row["name"], row["grade"])
```

You write that line right after connecting; the `cursor` has to be taken
afterwards.

## What comes next

The commands here are SQL's base layer. On the SQL path, `JOIN` is built on
top of them — combining two tables. That cannot be learned without this
knowledge either.
