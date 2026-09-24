**Idea:** Find the GCD with Euclid's algorithm, and count the tiles by dividing the areas.

**Step 1 — Euclid.**

$$
\begin{aligned}
840 &= 360 \cdot 2 + 120 \\
360 &= 120 \cdot 3 + 0
\end{aligned}
$$

The remainder is $0$: the GCD is $120$.

**Step 2 — Areas.** The floor area is $360 \cdot 840$, a tile's area $120 \cdot 120$. The number of tiles is the ratio of the areas:

$$
\frac{360 \cdot 840}{120 \cdot 120} = \frac{360}{120} \cdot \frac{840}{120} = 3 \cdot 7 = 21
$$

We divided each side by $120$ before computing any large products.

**Why the same result?** Dividing the areas is the same as multiplying the numbers of tiles along the two sides; splitting the fraction into two factors shows this plainly. Euclid reaches the same GCD without factorising.

**Answer:** $120$ and $21$.
