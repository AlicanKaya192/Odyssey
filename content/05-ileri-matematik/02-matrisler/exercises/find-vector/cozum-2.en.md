**Idea:** Look at the same product through the columns. $A\mathbf{x}$ is a weighted sum of the columns of $A$, with the components of $\mathbf{x}$ as weights. So the question becomes: with which coefficients do I build $(7, 2)$ from the columns $(2, 1)$ and $(1, -1)$?

**Step 1 — Write it with columns.**

$$
x_1 \begin{bmatrix} 2 \\ 1 \end{bmatrix} + x_2 \begin{bmatrix} 1 \\ -1 \end{bmatrix} = \begin{bmatrix} 7 \\ 2 \end{bmatrix}
$$

**Step 2 — Match the components.** Top components: $2x_1 + x_2 = 7$. Bottom components: $x_1 - x_2 = 2$.

**Step 3 — Isolate $x_1$ from the bottom equation.**

$$
x_1 = 2 + x_2
$$

**Step 4 — Put it into the top equation.**

$$
\begin{aligned}
2(2 + x_2) + x_2 &= 7 \\
4 + 2x_2 + x_2 &= 7 \\
3x_2 &= 3 \\
x_2 &= 1
\end{aligned}
$$

So $x_1 = 2 + 1 = 3$.

**Check:** Add the columns with these coefficients:

$$
\begin{aligned}
3 \begin{bmatrix} 2 \\ 1 \end{bmatrix} + 1 \begin{bmatrix} 1 \\ -1 \end{bmatrix} &= \begin{bmatrix} 6 \\ 3 \end{bmatrix} + \begin{bmatrix} 1 \\ -1 \end{bmatrix} \\
&= \begin{bmatrix} 7 \\ 2 \end{bmatrix}
\end{aligned}
$$

It holds. ✓

**What did we see?** "Solve $A\mathbf{x} = \mathbf{b}$" and "build $\mathbf{b}$ from the columns of $A$" are the same question. In the Gaussian elimination section we will do this with a systematic method for large systems.

**Answer:** $x_1 = 3$, $x_2 = 1$.
