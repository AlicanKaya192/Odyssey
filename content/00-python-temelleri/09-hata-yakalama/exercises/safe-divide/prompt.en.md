You have a total and a list of numbers:

```python
total = 100
numbers = [10, 5, 0, 4]
```

You are going to print `total / number` for each number. But there is a `0`
in the list, and dividing by zero raises an error:

```
ZeroDivisionError: division by zero
```

The program must not stop because of it. When you reach that number and
cannot print a result, print `undefined` and **carry on through the list**.

**What to do:**

1. Walk the list with a loop.
2. Put the division inside a `try` block.
3. When a `ZeroDivisionError` appears, print `undefined` instead of a result.

**Expected output:**

```
10.0
20.0
undefined
25.0
```

The results are decimals because `/` always gives a decimal number.

> You could get this output with `if number != 0:` as well, but this exercise
> is about `try` / `except`; that is what the check looks for.
