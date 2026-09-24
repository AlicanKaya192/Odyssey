**What is asked?** The area between two curves, and the area between a curve and the axis.

**Idea:** The area between two curves is $\int (\text{top} - \text{bottom}) \, dx$. For the area between a curve and the axis, first find where the curve crosses the axis.

**Step 1 — The first area.** On $[0, 1]$, $x \ge x^2$:

$$
\int_0^1 (x - x^2) \, dx = \left[\frac{x^2}{2} - \frac{x^3}{3}\right]_0^1 = \frac{1}{2} - \frac{1}{3} = \frac{1}{6}
$$

**Step 2 — The limits.** $4 - x^2 = 0 \Rightarrow x = -2$, $x = 2$. In between, $f \ge 0$.

**Step 3 — The second area.**

$$
\left[4x - \frac{x^3}{3}\right]_{-2}^{2} = \left(8 - \frac{8}{3}\right) - \left(-8 + \frac{8}{3}\right) = \frac{32}{3}
$$

**Check:** The second area is two thirds of the rectangle with base $4$ and height $4$ ($16$): a parabolic segment always has this area (Archimedes) ✓.

**Watch out:** Writing $\int (x^2 - x)$ in the first gives $-\frac{1}{6}$; an area must be positive, so subtract the bottom curve from the top one.

**Answer:** $\frac{1}{6}$ and $\frac{32}{3}$.
