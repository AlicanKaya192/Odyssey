So far you have measured the model with numbers. This time you will **see
it.**

A single-feature model learns a line. Put the test points and that line on
the same chart, and where the model holds up and where it misses becomes
visible.

**What you need to do:**

1. Read the file, take `area` and `price`, split it the same way
   (`random_state=42`), train the model and produce the test predictions.
2. Draw the test points as a **scatter**: `X_test` across, `y_test` up.
3. Draw the model's line on top: `X_test` across, the **predictions** up.
   Make it red so it stands out from the points.
4. Label the axes `area` and `price`, and add a title.
5. Save the chart as **`chart.png`**.
6. Print the model's **R²** to three decimals.

**Expected output:**

```
0.943
```

After you run it, your chart will appear **in the results panel**.

**What you will see in the chart:** the points scattered around the red
line. Where a point sits on the line the model was right; where it sits far
away the model was wrong. R² 0.943 is that spread turned into a number.

There is a reason some points stay far off: price does not depend on area
alone but on age too — and this model does not know about age. Adding age in
the previous exercise brought the error down from 18.5 to 7.13. **This chart
is a picture of that gap.**

**Note:** you do not need `plt.show()`; there is no screen here, you are
saving to a file.
