The previous exercise showed you three thresholds. Now you will see **all**
of them and put the trade-off on a chart.

**What you need to do:**

1. Build the same flow, train the model, take the positive class's
   probability.
2. Produce thresholds from **0.05 to 0.95** in steps of five hundredths.
3. Compute precision and recall for each, collecting them in two separate
   lists.
4. Draw both curves on the same chart: threshold across, score up. Label the
   curves `precision` and `recall` and add the **legend**.
5. Label the axes `threshold` and `score`, add a title, save as
   `chart.png`.
6. Print the **highest threshold that keeps recall at 0.9 or above**.

**Expected output:**

```
0.65
```

Your chart will appear **in the results panel** after you run it.

**What you will see are two opposing curves:** precision rising from left to
right, recall falling. Where they cross is the point of balance.

**The 0.65 you printed is a decision.** "Recall must be at least 90%" is a
constraint; this is the threshold that pushes precision as high as possible
under it. Real projects decide exactly this way: **put a floor under one
side and optimise the other.**

Whoever builds the model cannot invent that floor alone. The sentence "we
can afford to miss at most 10% of the students who will pass" comes from the
person doing the work; it is a domain decision, not an engineering one.

**One warning:** we chose the threshold here by looking at the test set. In
a real project that would turn the test into training data — a threshold is
chosen on a **validation** set, and you look at the test set once, at the
end. That is section 5.
