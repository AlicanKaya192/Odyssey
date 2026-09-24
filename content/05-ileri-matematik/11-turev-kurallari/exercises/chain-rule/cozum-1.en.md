**What is asked?** The value at $x = 1$ of the derivatives of two nested functions.

**Idea:** The chain rule: the derivative of the outer function (inside unchanged) times the derivative of the inner function.

**Step 1 — $y'$.** $y' = 4(2x^2 - 3)^3 \cdot 4x = 16x(2x^2 - 3)^3$.

**Step 2 — $y'(1)$.** $16 \cdot 1 \cdot (-1)^3 = -16$.

**Step 3 — $z'$.** $z' = e^{-x^2/2} \cdot (-x)$; $z'(1) = -e^{-1/2} \approx -0.6065 \approx -0.607$.

**Check:** At $x = 1$, $2x^2 - 3 = -1$; values of $y$ around $1$: $y(1.01) = (-0.9598)^4 \approx 0.8486$, $y(0.99) = (-1.0398)^4 \approx 1.1690$. The difference over $0.02$: $\approx -16.0$ ✓.

**Watch out:** Forgetting the inner derivative gives $y' = 4(2x^2 - 3)^3$, which is $-4$ at $x = 1$; four times too small.

**Answer:** $y'(1) = -16$, $z'(1) \approx -0.607$.
