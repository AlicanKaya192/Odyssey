**What is asked?** The side of the cut square that makes the box's volume largest.

**Idea:** Write the volume in terms of $x$ and set its derivative to zero. Taking out the common factor in the derivative shows the roots at once.

**Step 1 — The volume.** $V(x) = x(12 - 2x)^2$, $0 < x < 6$.

**Step 2 — The derivative.** The product rule, with a chain in the second factor: $\big((12 - 2x)^2\big)' = 2(12 - 2x) \cdot (-2)$.

$$
\begin{aligned}
V'(x) &= (12 - 2x)^2 - 4x(12 - 2x) \\
&= (12 - 2x)(12 - 6x)
\end{aligned}
$$

**Step 3 — The roots.** $x = 6$ (zero volume, no box) or $x = 2$.

**Step 4 — The volume.** $V(2) = 2 \cdot 8^2 = 128$.

**Check:** $V(1) = 1 \cdot 100 = 100$, $V(3) = 3 \cdot 36 = 108$. Both are below $128$ ✓.

**Watch out:** Forgetting the $-2$ from the chain rule gives a wrong expression such as $V' = (12 - 2x)(12 - 2x + 2x)$, and the critical point is lost.

**Answer:** $x = 2$ cm, $V = 128$ cm³.
