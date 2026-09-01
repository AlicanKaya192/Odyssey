Data arriving from somewhere else is rarely clean. The list you have holds
some values that convert to a number and some that do not:

```python
values = ["12", "7", "abc", "30", "5x"]
```

The call `int("abc")` raises a `ValueError`. The program must not stop because
of it; it should add up what converts and count what does not.

**What to do:**

1. Create two variables:

| Variable | What goes in it |
|---|---|
| `total` | The sum of the values that convert to a number |
| `skipped` | How many did not convert |

2. Walk the list. **Try** converting each value; when it does not work, count
   it and carry on.
3. Print `total` first, then `skipped`.

**Expected output:**

```
49
2
```

`12 + 7 + 30 = 49`; `"abc"` and `"5x"` do not convert.

> `"5x"` looks convertible at first glance, but `int()` wants **the whole**
> string to be a number. The letter at the end makes it a `ValueError` too.
