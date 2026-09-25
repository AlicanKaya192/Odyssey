**What is asked?** The overlapping area of two rectangles, their union and the ratio.

**Idea:** The intersection of two axis-parallel rectangles is the rectangle formed by the common part of the $x$ ranges and the common part of the $y$ ranges.

**Step 1 — The intersection.** $x$: the common part of $[1, 5]$ and $[3, 7]$ is $[3, 5]$, width $2$. $y$: the common part of $[1, 4]$ and $[2, 6]$ is $[2, 4]$, height $2$. The intersection is $2 \cdot 2 = 4$.

**Step 2 — The union.** The true box is $4 \cdot 3 = 12$, the prediction $4 \cdot 4 = 16$.

$$
12 + 16 - 4 = 24
$$

**Step 3 — IoU.** $\frac{4}{24} = \frac{1}{6} \approx 0.17$.

**Check:** IoU must be between $0$ and $1$ ✓; it is below $0.5$, so this prediction would usually not count as a "correct detection".

**Watch out:** Forgetting to subtract the intersection gives $28$ for the union; the shared region would be counted twice.

**Answer:** Intersection $4$, union $24$, $\text{IoU} = \frac{1}{6}$.
