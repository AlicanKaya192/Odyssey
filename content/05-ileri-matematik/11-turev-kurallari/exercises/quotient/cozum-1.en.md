**What is asked?** The value at a point of the derivative of a fraction, and where the derivative is zero.

**Idea:** $\left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2}$. If the derivative is zero, its top is zero.

**Step 1 — The derivative.**

$$
f'(x) = \frac{1 \cdot (x^2 + 1) - x \cdot 2x}{(x^2 + 1)^2} = \frac{1 - x^2}{(x^2 + 1)^2}
$$

**Step 2 — $f'(2)$.** $\frac{1 - 4}{25} = -\frac{3}{25} = -0.12$.

**Step 3 — The zero.** $1 - x^2 = 0 \Rightarrow x = \pm 1$; the positive one is $x = 1$.

**Check:** At $x = 1$, $f(1) = \frac{1}{2}$; $f(0.9) = \frac{0.9}{1.81} \approx 0.497$, $f(1.1) = \frac{1.1}{2.21} \approx 0.498$. Both sides are below $0.5$: $x = 1$ is a peak, so a zero derivative is just what we expect ✓.

**Watch out:** Swapping the order on top ($x \cdot 2x - (x^2 + 1)$) gives $f'(2) = +\frac{3}{25}$; at $x = 2$ the function is decreasing, so the derivative must be negative.

**Answer:** $f'(2) = -\frac{3}{25}$, $x = 1$.
