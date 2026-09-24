**What is asked?** The values of $k$ for which $A$ has no inverse. An inverse exists only when the determinant is non-zero, so we look for where the determinant is **zero**.

**Idea:** Write $\det A$ in terms of $k$, set it to zero and solve the resulting equation.

**Step 1 — The determinant.** With $ad - bc$:

$$
\begin{aligned}
\det A &= k \cdot (k + 1) - 4 \cdot 3 \\
&= k^2 + k - 12
\end{aligned}
$$

**Step 2 — Set it to zero.**

$$
k^2 + k - 12 = 0
$$

**Step 3 — Factorise.** Two numbers with product $-12$ and sum $+1$: $4$ and $-3$ ($4 \cdot (-3) = -12$, $4 + (-3) = 1$).

$$
(k + 4)(k - 3) = 0
$$

A product is zero only when one factor is zero: $k = 3$ or $k = -4$.

**Check:** For $k = 3$, $\begin{bmatrix} 3 & 4 \\ 3 & 4 \end{bmatrix}$ has determinant $12 - 12 = 0$ ✓. For $k = -4$, $\begin{bmatrix} -4 & 4 \\ 3 & -3 \end{bmatrix}$ has determinant $12 - 12 = 0$ ✓.

**Reading the result:** For **every** $k$ other than these two, $A$ is invertible.

**Answer:** positive $k = 3$, negative $k = -4$.
