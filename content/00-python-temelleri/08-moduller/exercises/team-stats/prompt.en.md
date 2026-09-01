You have the marks of a class:

```python
scores = [70, 85, 90, 60, 95, 80]
```

You are going to work out two numbers: the **mean** and the **median**. Both
are already there in the `statistics` module.

For this exercise you will not write `import statistics`. You will take the
functions **directly**, that is, with the `from ... import ...` form.

**What to do:**

1. Take the `mean` and `median` functions directly from the `statistics`
   module.
2. Create two variables:

| Variable | What goes in it |
|---|---|
| `average` | The mean of the marks |
| `middle` | The median of the marks |

3. Print the two of them **on separate lines**.

**Expected output:**

```
80
82.5
```

The median comes out as `82.5` because there are six marks; once sorted there
is no single number in the middle, so the midpoint of the middle two is taken.
