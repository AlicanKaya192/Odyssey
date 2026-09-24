**Idea:** The trapezoid rule is really the average of the left-end and right-end sums; find the two separately first.

**Step 1 — Left ends.** $0.5 \cdot (0 + 0.25 + 1 + 2.25) = 1.75$ (it undercounts).

**Step 2 — Right ends.** $3.75$ (it overcounts).

**Step 3 — The average.** $\frac{1.75 + 3.75}{2} = 2.75$. The true value $\frac{8}{3}$ lies between the two sums.

**Why the same result?** The area of a trapezoid is the average of the rectangle with the left height and the rectangle with the right height: $h \cdot \frac{f_i + f_{i+1}}{2}$. Adding them all up, the inner points appear twice; that is where the factors $2$ in the formula come from.

**Answer:** $3.75$, $2.75$, $\frac{8}{3}$.
