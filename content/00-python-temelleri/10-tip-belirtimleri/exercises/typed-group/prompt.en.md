This is the shape you will meet most often in real data work: the rows of a
table held as a list of dictionaries. In this exercise you will both group
them and write the annotations.

The data you have:

```python
people = [
    {"name": "Ada", "city": "London"},
    {"name": "Alan", "city": "London"},
    {"name": "Grace", "city": "New York"},
]
```

**What you need to do:**

1. Write a function called `group_by_city`:
   - Its parameter is `rows` — a list of dictionaries.
   - It returns a dictionary holding a **list of names** under each city.

2. Write a function called `first_name`:
   - Its parameters are `rows` and `city`.
   - It returns the **first** name in that city. If the city is not there at
     all, it returns `None`.
   - The return annotation must express both possibilities.

3. Print these in order:
   - `group_by_city(people)`
   - `first_name(people, "New York")`
   - `first_name(people, "Paris")`

**Expected output:**

```
{'London': ['Ada', 'Alan'], 'New York': ['Grace']}
Grace
None
```

> If a key is not in the dictionary yet you have to put an empty list there
> first: `if city not in result: result[city] = []`
