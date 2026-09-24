**What is asked?** Approximate calculation of two values with the tangent line.

**Idea:** At a known point ($\sqrt{4} = 2$, $1^{10} = 1$) the value and the derivative are easy; for a small step, the tangent is good enough.

**Step 1 — $\sqrt{4.1}$.** $f(4) = 2$, $f'(4) = \frac{1}{4}$, $h = 0.1$: $2 + 0.025 = 2.025$.

**Step 2 — $1.02^{10}$.** $g(x) = (1 + x)^{10}$, $g(0) = 1$, $g'(0) = 10$, $x = 0.02$: $1 + 0.2 = 1.2$.

**Check:** The true values are $2.02485$ and $1.21899$. The first approximation is very good; in the second the error is $0.019$, because curvature piles up over the tenth power. The second term $\frac{10 \cdot 9}{2} \cdot 0.02^2 = 0.018$ is almost all of that error ✓.

**Watch out:** Computing the derivative at $4.1$ instead of $4$ also works, but defeats the purpose; the approximation is made with what is known at the known point.

**Answer:** $2.025$ and $1.2$.
