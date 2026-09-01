In this exercise you will use several details of the `print` function
together: changing the separator, turning off the line break, and doing
arithmetic.

**What you need to do:**

1. Print three lines. On each line, the product name and its price are
   separated by a **full stop** — exactly as below:

```
apple.3
bread.5
milk.4
```

   Use the `sep` setting of the `print` function for this.

2. Then print `total:` on a line **without moving to the next line**, and
   straight after it print the sum of the three prices. Use the `end` setting
   for this.

**Expected output:**

```
apple.3
bread.5
milk.4
total:12
```

Note: there is **no space** between `total:` and `12` on the fourth line. Do
not type `12` yourself; let Python work it out.

> `print("a", "b", sep=".")` separates two values with a full stop.
> `print("x", end="")` does not move to the next line after printing.
