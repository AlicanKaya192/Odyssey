**What is asked?** How many steps along $\mathbf{b}_1$ and $\mathbf{b}_2$ reach the point $(5, 1)$? These numbers are the coordinates of $\mathbf{x}$ in the new basis.

**Idea:** Expand $c_1\mathbf{b}_1 + c_2\mathbf{b}_2$ into components and set it equal to $(5, 1)$. The basis vectors are independent, so there is exactly one solution.

**Step 1 — Write the components.**

$$
c_1 (1, 2) + c_2 (1, -1) = (c_1 + c_2,\ 2c_1 - c_2)
$$

**Step 2 — Match them.**

$$
\begin{aligned}
c_1 + c_2 &= 5 \\
2c_1 - c_2 &= 1
\end{aligned}
$$

**Step 3 — Add.** $c_2$ and $-c_2$ cancel:

$$
\begin{aligned}
3c_1 &= 6 \\
c_1 &= 2
\end{aligned}
$$

**Step 4 — $c_2$.** From the first equation, $c_2 = 5 - 2 = 3$.

**Check:**

$$
2 (1, 2) + 3 (1, -1) = (2 + 3,\ 4 - 3) = (5, 1)
$$

✓

**Reading the result:** The same point is $(5, 1)$ in the standard basis and $(2, 3)$ in the new one. The point did not change; the "rulers" describing it did.

**Answer:** $c_1 = 2$, $c_2 = 3$.
