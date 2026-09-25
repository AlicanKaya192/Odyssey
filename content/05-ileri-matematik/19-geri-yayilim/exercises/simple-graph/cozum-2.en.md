**Idea:** The expression is small; expand it, take the partial derivatives directly, and compare with the graph's result.

**Step 1 — Expand.** $f = xz + yz$.

**Step 2 — The partial derivatives.** $\frac{\partial f}{\partial x} = z = -4$, $\frac{\partial f}{\partial y} = z = -4$, $\frac{\partial f}{\partial z} = x + y = 3$.

**Why the same result?** The graph's rules "addition distributes, multiplication swaps" are exactly what these partial derivatives produce. For small expressions expanding is easy; for a network with millions of operations it is impossible, but the local rules of the graph work just the same.

**Answer:** $-4$, $-4$, $3$.
