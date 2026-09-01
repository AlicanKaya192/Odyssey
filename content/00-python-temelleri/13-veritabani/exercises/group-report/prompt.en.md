In this exercise you will let the database do the arithmetic rather than
Python.

**What you need to do:**

1. Connect to the `":memory:"` database, create the `students` table
   (`name TEXT`, `grade INTEGER`, `city TEXT`) and insert these rows:

```python
[
    ("Ada", 90, "London"),
    ("Brian", 40, "London"),
    ("Grace", 75, "New York"),
    ("Alan", 60, "London"),
    ("Edith", 95, "New York"),
]
```

2. Build a **dictionary** called `by_city`: the city name as the key and that
   city's **average rounded to a whole number** as the value. Let the database
   work out the average with `AVG`, using `GROUP BY city`.
   Bring the cities back in **alphabetical order**.

3. In a variable called `best_city`, hold the name of the city with the
   highest average.

4. Print `by_city` first, then `best_city`.

**Expected output:**

```
{'London': 63, 'New York': 85}
New York
```

London's average is `(90 + 40 + 60) / 3 = 63.33`, which rounds to `63`.
New York's is `(75 + 95) / 2 = 85.0`, which rounds to `85`.

Note: `AVG` returns a decimal number; you have to convert it with `round(...)`.

> Add `ORDER BY city` for the sorting. To find the highest, loop over the
> dictionary.
