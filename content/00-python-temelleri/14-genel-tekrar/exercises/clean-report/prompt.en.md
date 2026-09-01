Real data does not arrive clean. The `data.txt` file next to your code has
valid lines, an empty line and broken lines:

```
Ada,90
Brian,notanumber
Grace,75

Alan,60
Edith
```

**What you need to do:**

1. Read the file. Build a dictionary called `scores` from the **valid** lines
   only: the name as the key and the grade as a number.
2. Skip the empty lines.
3. Skip lines whose grade cannot be turned into a number (`ValueError`).
4. Skip lines with no comma too — unpacking raises a `ValueError` there.
5. Hold the number of **broken** lines skipped in a variable called `skipped`.
   Empty lines do not count as broken.
6. Print `scores` first, then `skipped`.

**Expected output:**

```
{'Ada': 90, 'Grace': 75, 'Alan': 60}
2
```

> `"Edith".split(",")` gives a one-element list, and trying to unpack that
> into two variables raises a `ValueError`. So a single `except ValueError`
> catches both situations.
