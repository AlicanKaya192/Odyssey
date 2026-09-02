You will put **two different charts** on one canvas: bars on the left, a
scatter plot on the right.

**What you need to do:**

1. Create a canvas with two drawing areas side by side, sized `(10, 4)`.
2. **On the left**, draw the city-score bar chart, force the axis to 0-100
   and set the title to `Scores`.
3. **On the right**, draw a **scatter plot** comparing study hours with the
   score; set the title to `Hours vs score` and the x axis to `Hours`.
4. Tighten the layout so the areas do not overlap.
5. Print, in order: the number of areas on the canvas, the number of bars on
   the left, both titles (joined with ` | `), and the upper bound of the left
   axis.

**Expected output:**

```
2
4
Scores | Hours vs score
100
```

**You are learning three things:**

- **One canvas can hold several drawing areas.** The general rule: one chart
  says **one thing**. If you have two things to say, draw two charts rather
  than cramming everything into one.
- A **scatter plot** shows the relationship between two numeric columns. Each
  point is a record. If the points form a line the two variables move
  together — but that **does not mean one causes the other.**
- `fig.tight_layout()` is almost always needed on multi-area canvases;
  without it the labels run into each other.
