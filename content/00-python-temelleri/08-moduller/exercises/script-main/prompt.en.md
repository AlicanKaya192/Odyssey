A Python file can be used in two ways: run directly, or imported from another
file. The line `if __name__ == "__main__":` separates those two cases.

**What you need to do:**

1. Import the `math` module.
2. Write a function called `area`: it takes a radius and returns the area of
   the circle **rounded to two decimal places**. The formula is `pi * r * r`.
3. Write a function called `main`: it prints the `area` result for each radius
   in the list `[1, 2, 3]`.
4. Put the guard line at the bottom and call `main()`:

```python
if __name__ == "__main__":
    main()
```

**Expected output:**

```
3.14
12.57
28.27
```

The guard line means: "run `main()` if this file was run directly; do not run
it if another file imported this one." That way the functions in your file can
be used by others without any side effects.

> `math.pi` gives you the number, and `round(value, 2)` rounds to two decimal
> places.
