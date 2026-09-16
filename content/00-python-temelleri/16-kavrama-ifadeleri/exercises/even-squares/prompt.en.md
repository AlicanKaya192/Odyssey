You will see the two faces of a comprehension on the same data: a
**filter** drops elements, a **conditional value** writes something for
every element.

The data you have:

```python
numbers = [1, 2, 3, 4, 5, 6]
```

**What to do — write both with comprehensions:**

1. `squares` — the squares of the **even** numbers only.
2. `labels` — `"even"` or `"odd"` for every number.

Then print them in order.

**Expected output:**

```
[4, 16, 36]
['odd', 'even', 'odd', 'even', 'odd', 'even']
```

> The filter goes at the end (`... if n % 2 == 0`) and the conditional
> value at the front (`"even" if ... else "odd" for ...`).
