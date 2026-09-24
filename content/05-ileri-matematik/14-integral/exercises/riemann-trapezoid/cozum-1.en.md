**What is asked?** Two numerical approximations of the same integral, and the true value.

**Idea:** Compute the values at the points once; both formulas add them up with different weights.

**Step 1 — Right ends.** $0.5 \cdot (0.25 + 1 + 2.25 + 4) = 0.5 \cdot 7.5 = 3.75$.

**Step 2 — Trapezoid.** $\frac{0.5}{2}(0 + 0.5 + 2 + 4.5 + 4) = 0.25 \cdot 11 = 2.75$.

**Step 3 — The true value.** $\left[\frac{x^3}{3}\right]_0^2 = \frac{8}{3} \approx 2.667$.

**Check:** The errors: $1.083$ for the right ends, $0.083$ for the trapezoid. For an increasing function the right ends always overcount; the trapezoid largely corrects this ✓.

**Watch out:** In the trapezoid rule the inner points count twice and the end points once; counting them all twice leads to a wrong value such as $0.25 \cdot 15 = 3.75$.

**Answer:** $3.75$, $2.75$ and $\frac{8}{3}$.
