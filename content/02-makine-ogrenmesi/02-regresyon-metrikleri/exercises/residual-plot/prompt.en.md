In the previous exercise you saw the model fail worst on a 26-year-old
house. That was one record; now you will see whether it is a **pattern**.

This time you compute the residuals on the **training** data. The rule has
not changed: you are not **measuring** there, you are **diagnosing**. Thirty
records give a clearer picture than ten, and the test set stays untouched
for measurement.

**What you need to do:**

1. Read, take `area` and `price`, split (`random_state=42`), train the model.
2. Compute the **training** residuals: `y_train - model.predict(X_train)`.
3. Take the **ages** of the training rows.
4. Draw the residuals against age as a **scatter**.
5. Add the zero line in red — a pattern can only be read against it.
6. Label the axes `age` and `residual`, add a title, save as `chart.png`.
7. Print the **correlation** between residual and age to three decimals.

**Expected output:**

```
-0.937
```

Your chart will appear **in the results panel** after you run it.

**That number says a great deal.** -0.937 is almost a perfect inverse
relationship: as age goes up the residual goes down, meaning the model
predicts **systematically too high**. A random scatter would put the
correlation near zero.

**What you will see in the chart** is the points forming a cloud that falls
from left to right. It is not a cloud but a trend line — and the last thing
you want to see in a model's residuals.

**Seeing a pattern in the residuals is not bad news but a road map.** A
pattern means something learnable is still sitting there. Here it is
obvious: the `age` column. When we added it in section 01 the error dropped
from 18.5 to 7.13 — this chart was saying so **before** we added it.

The way to improve a model usually runs not through trying something more
complex but through listening to what the residuals say.
