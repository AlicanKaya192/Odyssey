**What is asked?** The vector we get by multiplying the matrix $A$ by the vector $\mathbf{x}$.

**Idea:** Look at the sizes first: $A$ is $2 \times 3$ (2 rows, 3 columns), $\mathbf{x}$ has 3 components. The number of columns matches the vector's length, so the product is defined. The result has as many components as $A$ has rows, so **2 components**.

Each component of the result is the dot product of one row of $A$ with $\mathbf{x}$ (the row view): multiply matching numbers and add.

**Step 1 — Row 1.** $(1, -2, 0)$ with $(4, 1, -1)$:

$$
\begin{aligned}
1 \cdot 4 + (-2) \cdot 1 + 0 \cdot (-1) &= 4 - 2 + 0 \\
&= 2
\end{aligned}
$$

**Step 2 — Row 2.** $(3, 1, 2)$ with $(4, 1, -1)$:

$$
\begin{aligned}
3 \cdot 4 + 1 \cdot 1 + 2 \cdot (-1) &= 12 + 1 - 2 \\
&= 11
\end{aligned}
$$

**Step 3 — Write the result.** Row 1's result is the top component, row 2's the bottom one:

$$
A\mathbf{x} = \begin{bmatrix} 2 \\ 11 \end{bmatrix}
$$

**Watch out:** The result has 2 components, not 3. The output's length equals the matrix's number of rows; the number of columns only decides whether the product is defined.

**Answer:** $A\mathbf{x} = (2, 11)$.
