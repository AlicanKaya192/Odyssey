**Idea:** Write the normal equations as a system in two unknowns and solve by Gaussian elimination.

**Step 1 — System.** $4w_1 + 2w_2 = 10$ and $2w_1 + 2w_2 = 6$. The determinant is $4 \neq 0$, so there is a unique solution.

**Step 2 — $w_1$.** Subtract the second from the first: $2w_1 = 4$, $w_1 = 2$.

**Step 3 — $w_2$.** $2 \cdot 2 + 2w_2 = 6$, $w_2 = 1$.

**Why the same result?** Multiplying by the inverse and elimination are two ways of solving the same linear system; for large systems elimination (or QR) is cheaper and more stable than inverting.

**Answer:** $4$, $2$ and $1$.
