**Idea:** Substitute the intermediate variables and write $z$ directly as a function of $t$, then take a one-variable derivative.

**Step 1 — Substitute.** $z = (2t)^2 (t^2 + 1) = 4t^4 + 4t^2$.

**Step 2 — Differentiate.** $\frac{dz}{dt} = 16t^3 + 8t$; at $t = 1$, $24$.

**Step 3 — The partial derivative.** $\frac{\partial z}{\partial x} = 2xy$; at $(2, 2)$, $8$.

**Why the same result?** Expanding the two roads, $2xy \cdot x' = 8t(t^2 + 1)$ and $x^2 y' = 8t^3$, adds up to $16t^3 + 8t$: substitution merges the two roads into one formula. In neural networks substitution is impossible (millions of intermediate variables), so the chain rule adds the roads one by one.

**Answer:** $24$ and $8$.
