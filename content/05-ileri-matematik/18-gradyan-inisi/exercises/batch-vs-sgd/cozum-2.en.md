**Idea:** Find the full gradient by writing the average loss as a polynomial in $w$, without separating the examples; for SGD, write the example losses separately.

**Step 1 — The average loss.** $L = \frac{1}{2}\big((2 - w)^2 + (3 - 3w)^2\big) = \frac{1}{2}(10w^2 - 22w + 13)$. $L'(w) = 10w - 11$; $L'(0) = -11$.

**Step 2 — The full step.** $0 + 0.05 \cdot 11 = 0.55$.

**Step 3 — SGD.** $\ell_2 = 9(1 - w)^2$, $\ell_2' = -18(1 - w)$; $-18$ at $w = 0$, giving $w = 0.9$. $\ell_1 = (2 - w)^2$, $\ell_1'(0.9) = -2.2$; $w = 1.01$.

**Why the same result?** The derivative of an average is the average of the derivatives: $10w - 11 = \frac{1}{2}\big(-2(2 - w) - 18(1 - w)\big)$. The explicit formula also gives the best point: $L' = 0 \Rightarrow w = 1.1$.

**Answer:** $-11$, $0.55$, $1.01$.
