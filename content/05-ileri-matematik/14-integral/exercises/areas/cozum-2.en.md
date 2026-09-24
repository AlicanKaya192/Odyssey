**Idea:** Find the first area as the difference of two known areas, and the second over half the interval using symmetry.

**Step 1 — Triangle minus parabola.** Under $y = x$ on $[0, 1]$ there is a triangle: area $\frac{1}{2}$. Under $y = x^2$, $\int_0^1 x^2 = \frac{1}{3}$. The part in between is $\frac{1}{2} - \frac{1}{3} = \frac{1}{6}$.

**Step 2 — Symmetry.** $4 - x^2$ is an even function ($f(-x) = f(x)$): the left and right halves are equal. $\int_0^2 (4 - x^2) \, dx = 8 - \frac{8}{3} = \frac{16}{3}$.

**Step 3 — Twice that.** $2 \cdot \frac{16}{3} = \frac{32}{3}$.

**Why the same result?** Linearity, $\int (f - g) = \int f - \int g$; the first way took the difference in one integral, this way in two separate areas. Symmetry is a special case of joining intervals: two equal halves.

**Answer:** $\frac{1}{6}$ and $\frac{32}{3} \approx 10.667$.
