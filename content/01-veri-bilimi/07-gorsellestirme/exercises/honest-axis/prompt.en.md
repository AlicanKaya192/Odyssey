You will save the same chart twice: once **misleading**, once **honest**.
Seeing the two next to each other makes the difference stick.

The data is `students.csv` again:

```text
name,city,age,hours,score
Ada,Ankara,21,12,82
Kerem,Izmir,23,6,74
Mina,Ankara,22,14,91
Deniz,Bursa,25,4,68
Efe,Ankara,21,11,88
Sila,Izmir,24,8,76
...
```

**What to do:**

1. Read the file, work out the average score per city and draw it as a bar
   chart. Set the title to `Average score by city`.
2. Squeeze the y axis **between 68 and 90** and save it as
   **`misleading.png`**. Print the lower and upper limits side by side as
   whole numbers.
3. On the same chart, open the axis **from 0 to 100** and save it as
   **`honest.png`**. Print the limits again.
4. Print the ratio of the highest average to the lowest with two decimals.

**Expected output:**

```
68 90
0 100
1.22
```

Once you run it, both charts appear in the **results panel**.

**The ratio is close to 1.2:** the best city is about 20% ahead of the
worst. Now look at `misleading.png` — there the gap looks **several times**
bigger. The bottom of the axis was cut off, so the **length** of a bar is no
longer in proportion to its value.

**The rule:** start the axis of a bar chart at zero. Line charts do not have
this rule; there the point is the trend, not the size.
