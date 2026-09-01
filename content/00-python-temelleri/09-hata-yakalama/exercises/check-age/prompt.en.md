So far you have been catching errors. In this exercise **you will raise
one**.

You are going to write a function called `check_age`. A negative age is a
meaningless value; instead of quietly returning zero the function should
raise an error.

**What to do:**

1. Write the function `check_age(age)`:
   - When the age is **negative**, raise a `ValueError` whose message is
     exactly: `age cannot be negative`
   - Otherwise return the age as it is.

2. Pass each value to the function in the loop below:

```python
for value in [25, -3, 40]:
```

   - When a result comes back, print it.
   - When a `ValueError` appears, print **the error's message**.

**Expected output:**

```
25
age cannot be negative
40
```

Note: zero is not negative, so `check_age(0)` must not fail — it should
return `0`.

> To reach the error's message you write `except ValueError as error:` and
> then `print(error)`.
