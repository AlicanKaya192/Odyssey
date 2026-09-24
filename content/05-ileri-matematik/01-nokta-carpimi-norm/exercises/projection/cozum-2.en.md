**Idea:** Instead of memorising formulas, think in two simple moves: "take the direction, stretch it to the shadow's length". First capture the direction of $\mathbf{b}$ with an arrow of length 1. The dot product of a vector with a unit vector gives the length of its shadow in that direction directly.

**Step 1 — The unit vector along $\mathbf{b}$.** $\|\mathbf{b}\| = \sqrt{9 + 16} = 5$; divide every component by 5:

$$
\hat{\mathbf{b}} = \frac{(3,\ 4)}{5} = (0.6,\ 0.8)
$$

**Step 2 — The shadow's length.** Since $\hat{\mathbf{b}}$ has length 1, $\mathbf{a} \cdot \hat{\mathbf{b}} = \|\mathbf{a}\|\cos\theta$, which is exactly the shadow length:

$$
\begin{aligned}
\mathbf{a} \cdot \hat{\mathbf{b}} &= 6 \cdot 0.6 + 2 \cdot 0.8 \\
&= 3.6 + 1.6 = 5.2
\end{aligned}
$$

**Step 3 — The shadow itself.** Multiply the length-1 direction arrow by $5.2$; the direction stays, the length becomes $5.2$:

$$
\begin{aligned}
5.2 \cdot (0.6,\ 0.8) &= (5.2 \cdot 0.6,\ 5.2 \cdot 0.8) \\
&= (3.12,\ 4.16)
\end{aligned}
$$

**Why the same result?** The formulas of the first method are these two moves merged into one: $\dfrac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{b} \cdot \mathbf{b}}\,\mathbf{b} = (\mathbf{a} \cdot \hat{\mathbf{b}})\,\hat{\mathbf{b}}$. With the unit vector at hand, no division is needed at all.

**Answer:** $5.2$ and $(3.12,\ 4.16)$.
