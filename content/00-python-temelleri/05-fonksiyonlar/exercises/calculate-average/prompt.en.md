This exercise brings two topics together: functions and loops.

Define a function called `calculate_average`. It takes a single parameter: a list
of numbers. The function should work out the **average** of those numbers and
hand it back with `return`.

The average is the total divided by how many items there are. Accumulate the
total **with a loop**, and count the items in the same loop. Do not use the
built-in `sum()`.

Then call the function with this list:

```python
scores = [10, 20, 30, 40]
```

Put the result into `average` and print it. Expected output:

```
25.0
```

> Getting `25.0` rather than `25` is correct: the `/` operator always gives a
> decimal result.
