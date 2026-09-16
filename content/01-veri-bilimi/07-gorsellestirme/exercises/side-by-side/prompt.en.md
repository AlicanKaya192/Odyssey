You will put **two charts** on one figure: city averages on the left, the
link between study hours and score on the right.

The data is `students.csv`:

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

1. Write the imports, read the file and work out the average score per
   city.
2. Create a figure with two axes side by side, size `(10, 4)`.
3. **On the left**, draw the averages as bars, open the axis from 0 to 100
   and set the title to `Average score`.
4. **On the right**, draw `hours` against `score` as a **scatter plot**;
   title `Hours vs score`, x axis `Hours`, y axis `Score`.
5. Tighten the layout so the axes do not overlap and save it as
   **`panels.png`**.
6. Print, in order: the number of axes on the figure, the two titles (with
   ` | ` between them), and the correlation between hours and score (two
   decimals).

**Expected output:**

```
2
Average score | Hours vs score
0.96
```

Once you run it, your chart appears in the **results panel**.

**Three things to take away:**

- **One chart tells one story.** If you have two things to say, draw two
  charts instead of cramming everything into one.
- **Each point in a scatter plot is one student.** The points on the right
  form a line rising to the right; a correlation close to 1 is that picture
  turned into a number. But it **does not show that one causes the
  other.**
- `fig.tight_layout()` is nearly always needed on figures with several
  axes; otherwise the labels run into each other.
