In the previous section you searched for a threshold with a loop. Now you
will do the same job in three lines — and call a library for the first time.

You have the floor area and price of eight houses.

**What you need to do:**

1. Import the `LinearRegression` class from `sklearn.linear_model`.
2. Turn the `areas` list into the shape the model expects: **each number in
   its own row**, because `X` has to be a table.
3. Build a model and train it with `fit`.
4. Print the **slope** it learned to two decimals (`coef_`, its first item).
5. Print the **intercept** it learned to two decimals (`intercept_`).
6. Print the prediction for a **95 square metre** house to two decimals.

**Expected output:**

```
2.43
33.35
264.17
```

The first two lines are the rule the model learned:

```
price = 2.43 x area + 33.36
```

The third line is that rule applied to an input **that is not in the data**.
There is a 90 and a 100, but no 95 — the model produced the value in
between from the rule.

**Note:** you write the `import` line yourself. From this section on the
starter code gives no ready-made imports; knowing where each thing comes
from is part of the job.
