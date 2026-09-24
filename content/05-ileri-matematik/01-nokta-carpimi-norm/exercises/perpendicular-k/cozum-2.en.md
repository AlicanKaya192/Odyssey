**Idea:** In the plane there is **exactly one direction** perpendicular to a vector. If we find that direction, $\mathbf{a}$ has to be a multiple of it, and the known second component tells us which multiple. No equation needed.

**Step 1 — Find the perpendicular direction.** In the plane, a vector perpendicular to $(p, q)$ is obtained by swapping the components and flipping one sign: $(-q,\ p)$. Why? The dot product is $p \cdot (-q) + q \cdot p = 0$.

For $\mathbf{b} = (4, -2)$, $p = 4$ and $q = -2$:

$$
(-q,\ p) = \big(-(-2),\ 4\big) = (2,\ 4)
$$

**Step 2 — $\mathbf{a}$ lies along this direction.** Since $\mathbf{a}$ is also perpendicular to $\mathbf{b}$, it points along $(2, 4)$, so for some number $c$, $\mathbf{a} = c\,(2,\ 4) = (2c,\ 4c)$.

**Step 3 — Find the multiple.** The second component of $\mathbf{a}$ is given as $3$:

$$
\begin{aligned}
4c &= 3 \\
c &= \frac{3}{4}
\end{aligned}
$$

**Step 4 — The first component.**

$$
k = 2c = 2 \cdot \frac{3}{4} = \frac{3}{2} = 1.5
$$

**Check:** $(1.5,\ 3) \cdot (4,\ -2) = 6 - 6 = 0$. ✓

**When does it work?** This shortcut only holds in the plane (two dimensions). In three dimensions there are infinitely many directions perpendicular to a vector; there you set the dot product to zero as in the first method.

**Answer:** $k = 1.5$.
