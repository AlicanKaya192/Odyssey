**What is asked?** The determinant of $X^\mathsf{T}X$ for two data matrices. If it is zero, the inverse in the regression formula cannot be taken.

**Idea:** The $(i, j)$ entry of $X^\mathsf{T}X$ is the dot product of row $i$ of $X^\mathsf{T}$ and column $j$ of $X$. The rows of $X^\mathsf{T}$ are the columns of $X$, so this is **the dot product of columns $i$ and $j$ of $X$**.

The columns of $X_1$ are $\mathbf{c}_1 = (1, 2, 3)$ and $\mathbf{c}_2 = (2, 4, 6)$.

**Step 1 — $X_1^\mathsf{T}X_1$.**

$$
\begin{aligned}
\mathbf{c}_1 \cdot \mathbf{c}_1 &= 1 + 4 + 9 = 14 \\
\mathbf{c}_1 \cdot \mathbf{c}_2 &= 2 + 8 + 18 = 28 \\
\mathbf{c}_2 \cdot \mathbf{c}_2 &= 4 + 16 + 36 = 56
\end{aligned}
$$

$$
X_1^\mathsf{T}X_1 = \begin{bmatrix} 14 & 28 \\ 28 & 56 \end{bmatrix}
$$

**Step 2 — Its determinant.**

$$
14 \cdot 56 - 28 \cdot 28 = 784 - 784 = 0
$$

**Step 3 — $X_2^\mathsf{T}X_2$.** Column 2 is now $(2, 4, 7)$:

$$
\begin{aligned}
\mathbf{c}_1 \cdot \mathbf{c}_1 &= 14 \\
\mathbf{c}_1 \cdot \mathbf{c}_2 &= 2 + 8 + 21 = 31 \\
\mathbf{c}_2 \cdot \mathbf{c}_2 &= 4 + 16 + 49 = 69
\end{aligned}
$$

$$
X_2^\mathsf{T}X_2 = \begin{bmatrix} 14 & 31 \\ 31 & 69 \end{bmatrix}
$$

**Step 4 — Its determinant.**

$$
14 \cdot 69 - 31 \cdot 31 = 966 - 961 = 5
$$

**Reading the result:** In $X_1$ the second feature is exactly twice the first; both carry the same information and $X^\mathsf{T}X$ is singular. The inverse in the formula does not exist and the model cannot separate the two features' effects. Changing a single number ($6 \to 7$) makes the determinant $5$, and the inverse exists. But $5$ is a small number obtained as the difference of numbers like $966$: the columns are **almost** on one line and the weights will be unstable.

**Answer:** $0$ and $5$.
