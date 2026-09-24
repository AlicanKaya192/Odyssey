**What is asked?** Signed errors, and adding them up in three different ways.

**Idea:** The error $e = y - \hat{y}$ is a signed number: negative if the model predicted too high, positive if too low. The three sums differ in how they treat the signs.

**Step 1 — The errors.**

$$
\begin{aligned}
e_1 &= 10 - 13 = -3 \\
e_2 &= 7 - 6 = 1 \\
e_3 &= 12 - 9 = 3 \\
e_4 &= 5 - 8 = -3
\end{aligned}
$$

**Step 2 — The sum of the errors.** The positives give $1 + 3 = 4$, the negatives $-3 + (-3) = -6$:

$$
4 + (-6) = -2
$$

**Step 3 — The sum of absolute values.**

$$
3 + 1 + 3 + 3 = 10
$$

**Step 4 — The sum of squares.**

$$
(-3)^2 + 1^2 + 3^2 + (-3)^2 = 9 + 1 + 9 + 9 = 28
$$

**Reading the result:** A total error of $-2$ makes the model look almost perfect, yet every house is off by between $1$ and $3$ thousand. Absolute values and squares stop positive and negative errors from cancelling. Squares punish large errors more: an error of $3$ counts as $9$, while an error of $1$ counts as $1$.

**Answer:** $-2$, $10$ and $28$.
