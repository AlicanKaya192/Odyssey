A container can hold another container. In this exercise you will annotate
that.

**What you need to do:**

1. Define a dictionary called `grades` and write its annotation. The keys are
   strings and the **values are lists of numbers**. Starting value:

```python
{"Ada": [90, 85], "Alan": [70, 95]}
```

2. Write a function called `best`:
   - Its parameter is `records`, a dictionary in the same shape as `grades`.
   - It returns a dictionary with string keys and **single number** values.
   - It finds the **highest** grade in each person's list.

3. Print the result of `best(grades)`.

**Expected output:**

```
{'Ada': 90, 'Alan': 95}
```

Note: the parameter's annotation and the return annotation are **not the
same**. The incoming dictionary has lists as values; the outgoing one has
single numbers.

> `max(values)` gives you the largest value in a list.
