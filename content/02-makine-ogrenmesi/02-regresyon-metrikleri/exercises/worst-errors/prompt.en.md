Measures give you a single number. Now you will look behind that number and
find **which record** the model failed on worst.

**What you need to do:**

1. Build the usual flow: read, take `area` and `price`, split
   (`random_state=42`), train, produce the test predictions.
2. Compute the residuals (`actual - predicted`).
3. Print the **mean** of the residuals to two decimals.
4. Print the **largest absolute residual** to two decimals.
5. Print that record's **area and age** side by side, as whole numbers.
6. Print how many residuals are positive and how many negative, side by
   side.

**Expected output:**

```
-3.78
43.87
130 26
4 6
```

**The third line is what this exercise is really about.** The house the
model failed on worst is **26 years old** — one of the oldest in the
dataset. The model does not know about age, because we only put `area` into
`X`. That is exactly where it stumbles.

**Is this a coincidence or a pattern?** A single record cannot say. The next
exercise will plot every residual against age and answer it.

**The first line is a trap:** the mean residual is -3.78, close to zero.
That is **not** a sign of success. A linear regression's residuals balance
around zero by construction; it is a consequence of the method. You look at
the **spread**, not the mean.

**The last line** shows the balance: 4 positive, 6 negative. There is no
marked systematic bias — the problem is not in the direction but in the
size.
