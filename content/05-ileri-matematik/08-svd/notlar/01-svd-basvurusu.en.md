The short version of everything in the lesson. Come back here when you get stuck on a question.

## The decomposition

$$
A = U\Sigma V^\mathsf{T}, \qquad A\mathbf{v}_i = \sigma_i\mathbf{u}_i
$$

| Piece | Size ($A$: $m \times n$) | Property |
|---|---|---|
| $U$ | $m \times m$ | Orthogonal: $U^\mathsf{T}U = I$; columns are the left singular vectors |
| $\Sigma$ | $m \times n$ | Diagonal holds $\sigma_1 \ge \sigma_2 \ge \cdots \ge 0$ |
| $V$ | $n \times n$ | Orthogonal: $V^\mathsf{T}V = I$; columns are the right singular vectors |

Geometry: $V^\mathsf{T}$ rotates, $\Sigma$ stretches along the axes, $U$ rotates.
The unit circle goes to an ellipse with semi-axes $\sigma_i$.

## By hand

1. Compute $A^\mathsf{T}A$ (symmetric, $n \times n$).
2. Its eigenvalues are $\lambda_i \ge 0$; the singular values are $\sigma_i = \sqrt{\lambda_i}$, largest first.
3. Its eigenvectors, of unit length: $\mathbf{v}_i$.
4. $\mathbf{u}_i = A\mathbf{v}_i / \sigma_i$ (only for $\sigma_i \ne 0$).

$2 \times 2$ shortcut: $\sigma_1^2 + \sigma_2^2 = \operatorname{tr}(A^\mathsf{T}A)$ = the sum of the squares of all entries; $\sigma_1\sigma_2 = |\det A|$.

## What the singular values tell you

| Quantity | Value |
|---|---|
| Rank | number of non-zero $\sigma_i$ |
| Norm $\|A\|$ | $\sigma_1$ |
| $\lvert\det A\rvert$ (square) | $\prod \sigma_i$ |
| Sum of the squares of the entries | $\sum \sigma_i^2$ |
| Condition number | $\sigma_1 / \sigma_n$ |
| Symmetric, eigenvalues $\ge 0$ | $\sigma_i = \lambda_i$, $U = V$ |

## Layers and low-rank approximation

$$
A = \sum_{i=1}^{r} \sigma_i \mathbf{u}_i \mathbf{v}_i^\mathsf{T}
\qquad
A_k = \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^\mathsf{T}
$$

- $A_k$ is the closest matrix of rank $k$ (Eckart–Young).
- Error: $\|A - A_k\| = \sqrt{\sigma_{k+1}^2 + \cdots + \sigma_r^2}$.
- Energy kept: $\dfrac{\sigma_1^2 + \cdots + \sigma_k^2}{\sigma_1^2 + \cdots + \sigma_r^2}$.
- Storage: $k\,(m + n + 1)$ numbers (the original takes $m \cdot n$).

## A rank-1 matrix

If $A = \mathbf{a}\mathbf{b}^\mathsf{T}$, the only singular value is $\sigma_1 = \|\mathbf{a}\|\,\|\mathbf{b}\|$,
with $\mathbf{u}_1 = \mathbf{a} / \|\mathbf{a}\|$ and $\mathbf{v}_1 = \mathbf{b} / \|\mathbf{b}\|$.

## Practical tips

- Singular values are never negative; for a diagonal matrix take absolute values.
- You can use $AA^\mathsf{T}$ instead of $A^\mathsf{T}A$ (whichever is smaller): the non-zero eigenvalues are the same, and its eigenvectors are the $\mathbf{u}_i$.
- The $\mathbf{u}_i$ must come out perpendicular; if not, there is a mistake.
- For energy, add the **squares**, not the singular values.
