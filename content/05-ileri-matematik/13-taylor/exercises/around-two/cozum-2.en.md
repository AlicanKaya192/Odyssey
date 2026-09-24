**Idea:** Write $x = 2 + h$ and bring it to the expansion $\frac{1}{1 + u} = 1 - u + u^2 - \cdots$; no derivatives needed.

**Step 1 — Rearrange.**

$$
\frac{1}{2 + h} = \frac{1}{2} \cdot \frac{1}{1 + \frac{h}{2}}
$$

**Step 2 — Expand.** $\frac{1}{2}\left(1 - \frac{h}{2} + \frac{h^2}{4} - \cdots\right) = \frac{1}{2} - \frac{h}{4} + \frac{h^2}{8} - \cdots$. The coefficient of $h^2$ is $\frac{1}{8}$.

**Step 3 — The value.** $h = 0.2$: $0.5 - 0.05 + 0.005 = 0.455$.

**Why the same result?** The power series of a function around a point is unique: whichever road finds it, the coefficients come out the same. Reducing to a known expansion is often faster than computing the derivatives one by one.

**Answer:** $\frac{1}{8}$ and $0.455$.
