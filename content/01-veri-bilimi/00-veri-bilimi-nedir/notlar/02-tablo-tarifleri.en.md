# Table Recipes (without libraries)

The six operations you need most often on a list of dictionaries, in plain
Python. You can look here while you work on the exercises.

Every example uses this data:

```python
students = [
    {"name": "Ada", "city": "Ankara", "score": 82},
    {"name": "Kerem", "city": "Izmir", "score": 74},
    {"name": "Mina", "city": "Ankara", "score": 91},
    {"name": "Deniz", "city": "Izmir", "score": 68},
]
```

## 1. Pulling out a column

Getting every value of one column as a list:

```python
scores = [student["score"] for student in students]
print(scores)
```

```text
[82, 74, 91, 68]
```

In pandas this will be `data["score"]`.

## 2. The average

```python
scores = [student["score"] for student in students]
average = sum(scores) / len(scores)
print(average)
```

```text
78.75
```

**Trap:** if the list is empty, `len(scores)` is zero and you get a
`ZeroDivisionError`. This happens often with real data — after filtering
there may be no rows left.

```python
average = sum(scores) / len(scores) if scores else 0
```

In pandas this will be `data["score"].mean()`.

## 3. Filtering

Keeping the rows that match a condition:

```python
high = [student for student in students if student["score"] >= 80]
for student in high:
    print(student["name"])
```

```text
Ada
Mina
```

More than one condition:

```python
selected = [
    student
    for student in students
    if student["city"] == "Ankara" and student["score"] >= 80
]
```

In pandas this will be `data[data["score"] >= 80]`.

## 4. Sorting

```python
by_score = sorted(students, key=lambda student: student["score"])
print(by_score[0]["name"])
```

```text
Deniz
```

Largest first:

```python
by_score = sorted(students, key=lambda student: student["score"], reverse=True)
```

`sorted` returns a **new list**; the original is left alone.

In pandas this will be `data.sort_values("score")`.

## 5. Grouping

Splitting rows into buckets by a column:

```python
groups = {}
for student in students:
    city = student["city"]
    if city not in groups:
        groups[city] = []
    groups[city].append(student)

print(list(groups))
```

```text
['Ankara', 'Izmir']
```

You can write the same thing more briefly with `setdefault`:

```python
groups.setdefault(city, []).append(student)
```

In pandas this will be `data.groupby("city")`.

## 6. Computing per group

Grouping and aggregating together — the thing you need most often:

```python
totals = {}
counts = {}

for student in students:
    city = student["city"]
    totals[city] = totals.get(city, 0) + student["score"]
    counts[city] = counts.get(city, 0) + 1

averages = {city: totals[city] / counts[city] for city in totals}
print(averages)
```

```text
{'Ankara': 86.5, 'Izmir': 71.0}
```

`dict.get(key, 0)` makes this easier: if the key is missing it starts from
zero, so you do not need `if city not in totals`.

In pandas this will be `data.groupby("city")["score"].mean()`.

## Side by side

| Task | Plain Python | pandas (later sections) |
|---|---|---|
| Take a column | `[s["score"] for s in students]` | `data["score"]` |
| Average | `sum(scores) / len(scores)` | `data["score"].mean()` |
| Filter | `[s for s in students if ...]` | `data[data["score"] >= 80]` |
| Sort | `sorted(students, key=...)` | `data.sort_values("score")` |
| Group + compute | 8 lines | `data.groupby("city")["score"].mean()` |

The right column is short, but you cannot write it without knowing the left
one. When `groupby` gives you an error, you need to know what it was trying
to do.

## Formatting numbers

Averages usually come out with long decimals:

```python
average = 78.75333333333333
print(round(average, 2))
print(f"{average:.2f}")
```

```text
78.75
78.75
```

`round()` returns a **number**, f-string formatting returns **text**. Use
`round` if you are going to compare, an f-string if you are going to print.

**Trap:** `round(2.5)` is `2` and `round(3.5)` is `4`. On exact halves Python
rounds to the nearest **even** number. This is not a bug but a deliberate
choice (banker's rounding); it reduces bias over many values.
