A database's real job is answering questions. In this exercise you will ask
two questions without writing a loop in Python.

**What you need to do:**

1. Connect to the `":memory:"` database, create the `students` table
   (`name TEXT`, `grade INTEGER`, `city TEXT`) and insert these rows:

```python
[
    ("Ada", 90, "London"),
    ("Brian", 40, "London"),
    ("Grace", 75, "New York"),
    ("Alan", 60, "London"),
]
```

2. In a variable called `passing`, hold those with a **grade of 50 or above**,
   sorted by **grade, highest first**. Take only the `name` and `grade`
   columns.

3. In a variable called `londoners`, hold the **names of those whose city is
   London** as a list. Supply the city with the `?` placeholder.

4. Print `passing` first, then `londoners`.

**Expected output:**

```
[('Ada', 90), ('Grace', 75), ('Alan', 60)]
['Ada', 'Brian', 'Alan']
```

Note: the trailing comma in a one-element tuple is essential — `("London",)`.

> Filtering is done with `WHERE` and sorting with `ORDER BY ... DESC`.
