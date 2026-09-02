This exercise shows you a **chart lie**.

**What you need to do:**

1. Draw a bar chart of the cities and their scores.
2. Print whether the lower bound of the axis is zero (`True` or `False`).
3. Force the axis to run from **0 to 100**.
4. Print the new lower and upper bounds **side by side**, as whole numbers.

**Expected output:**

```
True
0 100
```

**In this data the axis already starts at zero** — the values run from 69 to
87 and matplotlib finds zero reasonable.

But if the values were 85, 87 and 88, the axis could start at 84 and the 3%
difference between them would look like **three times** on screen.

**The rule:** start the axis at zero on a bar chart. The reason: the
**length** of a bar represents the value. Cut off the bottom and the length
is no longer proportional to the value, and the chart lies.

The rule does not apply to line charts — there the subject is the trend, not
the absolute size.
