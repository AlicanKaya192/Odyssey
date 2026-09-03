You have seen what `k` does in numbers. Now you will **see it.**

The **decision boundary** a model draws shows which class is predicted for
each region of the plane. To draw it we use two features (`income` and
`visits`) — three dimensions cannot be drawn.

The grid and the scaling are ready in the starter code; your job is to build
the models and draw.

**What you need to do:**

1. Open two panels side by side (`plt.subplots(1, 2, figsize=(11, 4.5))`).
2. For the left panel **`k=1`** and the right panel **`k=15`**:
   - train the model on the scaled training data
   - predict for the ready-made `grid` and reshape to `grid_x`'s shape
   - colour the regions with `contourf` (`alpha=0.25`, `levels=1`)
   - put the training points on top with `scatter`, coloured by `y_train`
   - title `k = 1` / `k = 15`, axes `income (scaled)` and `visits (scaled)`
   - print one line with the test accuracy: **k, accuracy**
3. Call `fig.tight_layout()` and save as `chart.png`.

**Expected output:**

```
1 0.9
15 0.9
```

Your chart will appear **in the results panel** after you run it.

**The two numbers are identical. The two charts are nothing alike.**

**In the left panel (`k=1`)** the boundary is fragmented: little islands
around individual points. The model took every odd record seriously and
carved it its own region.

**In the right panel (`k=15`)** the boundary is a single smooth curve. Odd
records have dissolved into the majority.

**This is visual proof of why looking at one measure is not enough.** Both
have a test accuracy of 0.90; but one memorised the noise and the other
caught the general trend. When a new customer arrives the two will behave
very differently — and the left one will decide on the basis of coincidences
in the training data.

In section 02 we said "where a model is wrong matters as much as how often
it is right". This chart is another form of the same sentence: **how a model
decides matters as much as how often it is right.**
