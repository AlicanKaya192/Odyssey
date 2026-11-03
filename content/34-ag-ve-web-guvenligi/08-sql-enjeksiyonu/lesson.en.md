# SQL Injection

In the OWASP Top 10 section we put the heart of injection in one sentence:
**the user's data is interpreted as part of the code.** There we saw a
person with an apostrophe in their name break a query by accident. This
section explains why the same hole is so dangerous, why the lasting
solution is the **parameterised query**, and the three places where
parameters are not enough. All examples run with Python's `sqlite3` module
on small tables built **in memory**; no outside database is touched.

## When a query is built from text

An application wants to show a user's orders. It builds the query with an
f-string:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (id INTEGER, owner TEXT, item TEXT)")
conn.executemany("INSERT INTO orders VALUES (?, ?, ?)",
                 [(1, "ada", "book"), (2, "ada", "pen"),
                  (3, "bob", "laptop"), (4, "eve", "phone")])


def orders_bad(owner):
    query = f"SELECT item FROM orders WHERE owner = '{owner}'"
    return conn.execute(query).fetchall()


owner = "x' OR '1'='1"
print(orders_bad("ada"))
print(f"SELECT item FROM orders WHERE owner = '{owner}'")
print(len(orders_bad(owner)))
```

```text
[('book',), ('pen',)]
SELECT item FROM orders WHERE owner = 'x' OR '1'='1'
4
```

With a normal name it works correctly. But the `'` in the input closes the
text early and the rest (`OR '1'='1'`) is read as SQL. The resulting
query's condition is now true for every row: all the orders (4 rows),
including other people's, came back. The attacker changed not the data but
**the meaning of the query**. In the same way a password check in a login
form can be skipped or data in other tables read; how far the hole can be
taken depends on the application, but the root cause is always the same.

## The lasting solution: parameterised queries

Instead of pasting the data into the text, we send the query and the data
**separately**. In the query text a placeholder (`?`) stands where the
data goes; the database first parses the query, then puts the incoming
value in place **always as data**:

```python
def orders(owner):
    return conn.execute("SELECT item FROM orders WHERE owner = ?",
                        (owner,)).fetchall()


print(orders("ada"))
print(len(orders("x' OR '1'='1")))
```

```text
[('book',), ('pen',)]
0
```

The same input was now looked up only as "the owner whose name is
`x' OR '1'='1`", and no rows came back. What is inside the value no longer
matters: quotes, semicolons, SQL words are all part of the text. That is
why a parameterised query is far more solid than "filtering out dangerous
characters"; a filter list always forgets something, while a parameter
turns nothing into code.

<figure class="fig"><div class="versus">
  <div class="no"><h4>Joining text</h4><code>"... WHERE owner = '" + owner + "'"</code><br>The data is pasted into the query text; the characters in it can be read as SQL.</div>
  <div class="ok"><h4>Parameterised query</h4><code>"... WHERE owner = ?", (owner,)</code><br>The query and the data travel separately; data never becomes code.</div>
</div><figcaption>Queries built with an f-string, <code>+</code>, <code>%</code> or <code>.format</code> all belong to the group on the left.</figcaption></figure>

Note: `(owner,)` is a one-item **tuple**; if the comma is forgotten, Python
takes it as plain text. The form of the placeholder can differ between
libraries (`?`, `%s`, `:name`), but the idea is always the same. ORM
libraries also use parameters underneath; building a raw query from text
inside them brings the same hole back.

## Where parameters are not enough 1: column and table names

A placeholder stands only for **values**; it cannot stand for a column or
table name. When the user picks "sort by price", trying to give the column
name as a parameter silently works wrongly:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE products (name TEXT, price INTEGER)")
conn.executemany("INSERT INTO products VALUES (?, ?)",
                 [("pen", 3), ("book", 12), ("bag", 30), ("cup", 7)])

print(conn.execute("SELECT name FROM products ORDER BY ?", ("price",)).fetchall())

SORTABLE = {"name": "name", "price": "price"}


def products(sort):
    column = SORTABLE.get(sort, "name")
    return [r[0] for r in conn.execute(f"SELECT name FROM products ORDER BY {column}")]


print(products("price"))
print(products("rating"))
```

```text
[('pen',), ('book',), ('bag',), ('cup',)]
['pen', 'cup', 'book', 'bag']
['bag', 'book', 'cup', 'pen']
```

`ORDER BY ?` raised no error, but it did not sort either: the value was
taken as a constant text, and since it was the same for every row the
order stayed as inserted. The solution is an **allow list**: the user's
choice is only **mapped** to one of the known columns, and the text that
enters the query is always text we wrote. A choice not in the list
(`rating`) fell back to the default.

## Where parameters are not enough 2: LIKE wildcards

In a `LIKE` search `%` means "any text" and `_` means "any character". A
parameterised query does not turn the user's input into code, but these
characters still work as wildcards **in LIKE's own language**:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE notes (text TEXT)")
conn.executemany("INSERT INTO notes VALUES (?)",
                 [("50% discount",), ("500 pens",), ("plan_b",), ("planner",)])


def search(term):
    rows = conn.execute("SELECT text FROM notes WHERE text LIKE ?",
                        ("%" + term + "%",))
    return [r[0] for r in rows]


def escape_like(term):
    return term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def search_exact(term):
    rows = conn.execute("SELECT text FROM notes WHERE text LIKE ? ESCAPE '\\'",
                        ("%" + escape_like(term) + "%",))
    return [r[0] for r in rows]


print(search("%"))
print(search("0%"))
print(search_exact("0%"))
print(search("_"))
print(search_exact("_"))
```

```text
['50% discount', '500 pens', 'plan_b', 'planner']
['50% discount', '500 pens']
['50% discount']
['50% discount', '500 pens', 'plan_b', 'planner']
['plan_b']
```

The `%` search brought back every note; `0%` became "anything containing a
0". The wildcards were neutralised by putting an **escape character**
(`\`) in front of them, and `ESCAPE '\'` was added to the query; now `%`
and `_` are searched for as plain characters. The escape character itself
is escaped **first**; otherwise a `\` typed by the user neutralises the
next character. This hole leaks no data, but it makes the search work
wrongly, and a very wide `LIKE` pattern can tire the database on large
tables.

## Where parameters are not enough 3: second-order injection

A value is written safely with a parameter when it is first stored; but if
it is later **read back from the database** and added to another query as
text, the hole appears in that second query. The thought "this value
already comes from our own database" misleads: the value's source is still
the user. The rule is simple: in **every** query, wherever the value comes
from, a parameter.

## Limiting the damage

Even if a hole slips through somewhere, there are layers that make the
damage smaller:

- **Least privilege:** the application's database user can do only the
  needed operations on only the needed tables. A part that produces reports
  only reads:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE orders (item TEXT)")
conn.execute("INSERT INTO orders VALUES ('book')")
conn.execute("PRAGMA query_only = ON")

print(conn.execute("SELECT item FROM orders").fetchall())
try:
    conn.execute("DELETE FROM orders")
except sqlite3.OperationalError as error:
    print("refused:", error)
```

```text
[('book',)]
refused: attempt to write a readonly database
```

- **Hiding error details:** the database error message (table names, parts
  of the query) is not shown to the user; the user sees a general message
  and the details go into the server's log. A detailed error message helps
  an attacker work out the query step by step.
- **Input validation:** if an order number is an integer, it is turned into
  an integer first; an e-mail field is checked for e-mail form (the Input
  Validation section). This is a layer **next to** parameters, not
  **instead of** them.
- **WAF and monitoring:** can catch known patterns but can be bypassed (the
  Firewalls section); the real fix is in the code.

## Summary

- SQL injection: when a query is built from text, characters in the input
  change **the meaning of the query**; in the lesson all 4 orders came
  back.
- The **parameterised query** (`?` and separate values) is the lasting
  solution; whatever the value is, it stays data.
- A placeholder does not stand for **column and table names**: the user's
  choice is mapped to an **allow list**.
- Inside **LIKE**, `%` and `_` stay wildcards: escape the escape character
  first, then `%` and `_`, and write `ESCAPE`.
- Against **second-order** injection, a value from the database is used
  with a parameter too.
- Layers that limit the damage: a least-privileged database user, a
  general error message, input validation, monitoring.
