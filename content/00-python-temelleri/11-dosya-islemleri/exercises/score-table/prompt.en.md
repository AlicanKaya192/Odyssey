A file called `scores.txt` has been placed next to your code. Each line holds
a name and a grade separated by a comma, with one empty line in between.

```
Ada,90
Alan,70

Grace,85
Brian,60
```

**What you need to do:**

1. Read the file and build a dictionary called `scores`: the name as the key
   and the grade as a **number**. Skip the empty lines.
2. Hold the average of the grades in a variable called `average`, using
   **floor division**: `sum(...) // len(...)`
3. Hold the **name** of the person with the highest grade in a variable called
   `top`.
4. Print `scores`, `average` and `top` in that order.

**Expected output:**

```
{'Ada': 90, 'Alan': 70, 'Grace': 85, 'Brian': 60}
76
Ada
```

Note: everything read from a file arrives as **text**. `"90"` is not a number;
you have to convert it with `int()`.

> To split a line in two, use `line.split(",")`. To find the key holding the
> highest value you can loop through the dictionary and compare.
