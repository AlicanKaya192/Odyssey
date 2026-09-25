**What is asked?** A single gradient descent step in logistic regression.

**Idea:** $\frac{\partial\,\text{loss}}{\partial w} = (p - y)x$.

**Step 1 — $p$.** $z = 0.5 \cdot 2 - 0.5 = 0.5$. $p = \frac{1}{1.6065} \approx 0.622$.

**Step 2 — Derivative.** $(0.622 - 1) \cdot 2 \approx -0.755$.

**Step 3 — Update.** $w = 0.5 - 0.1 \cdot (-0.755) \approx 0.5755$.

**Check:** The new $z = 0.5755 \cdot 2 + b$; since $w$ increased, $z$ and $p$ increase and the loss ($-\ln p$) falls ✓.

**Watch out:** The gradient is negative; the update subtracts it, so $w$ grows. Writing the derivative as $(y - p)x$ and doing the same update sends $w$ the wrong way.

**Answer:** $\approx 0.622$, $\approx -0.755$, $\approx 0.5755$.
