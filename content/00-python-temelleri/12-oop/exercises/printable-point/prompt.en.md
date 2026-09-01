When you print an object directly you get something unreadable:

```
<__main__.Point object at 0x000001F3A2B4C110>
```

The `__str__` method fixes that.

**What you need to do:**

1. Write a class called `Point`. Its constructor takes `x` and `y`.
2. Write a `__str__` method: it **returns** the object as a string in the form
   `(3, 4)`.
3. Write a `distance` method: it returns the point's distance from the origin
   — the square root of the sum of the squares of `x` and `y`, **rounded to
   two decimal places.**
4. Build `Point(3, 4)`; print the object itself first, then the `distance`
   result.

**Expected output:**

```
(3, 4)
5.0
```

Note: `__str__` **returns** a string rather than printing one. If you write
`print` inside it, an extra `None` line appears.

> Use the `math` module for the square root: `math.sqrt(...)`. You need
> `str(...)` to put a number into a string.
