**What is asked?** A polynomial model's prediction at two points and its error on one example.

**Idea:** The prediction is the polynomial's value at that point. The error is the true value minus the prediction.

**Step 1 — $x = 2$.** $x^2 = 4$, $x^3 = 8$.

$$
\begin{aligned}
\hat{y} &= 1 + 2 \cdot 2 - 1 \cdot 4 + 0.5 \cdot 8 \\
&= 1 + 4 - 4 + 4 = 5
\end{aligned}
$$

**Step 2 — $x = -2$.** $x^2 = 4$, $x^3 = -8$.

$$
\begin{aligned}
\hat{y} &= 1 + 2 \cdot (-2) - 4 + 0.5 \cdot (-8) \\
&= 1 - 4 - 4 - 4 = -11
\end{aligned}
$$

**Step 3 — The error.** $y - \hat{y} = 6 - 5 = 1$. The model predicted $1$ unit too low on this example.

**Check:** The even-power terms ($1$ and $-x^2$) are the same at both points: $1 - 4 = -3$. The odd-power ones ($2x + 0.5x^3$) only change sign: $+8$ and $-8$. $-3 + 8 = 5$, $-3 - 8 = -11$ ✓.

**Watch out:** $w_2 = -1$ times $x^2 = 4$ is $-4$; do not confuse squaring a negative number ($(-2)^2$) with the minus of the coefficient.

**Answer:** $\hat{y}(2) = 5$, $\hat{y}(-2) = -11$, error $1$.
