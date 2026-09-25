A short version of everything in the lesson. Come back here when you get stuck on a question.

## Steps

1. Centre: $x \leftarrow x - \bar{x}$ (standardise if the units differ).
2. Covariance matrix $\Sigma = \frac{1}{n - 1}X^\mathsf{T}X$.
3. Eigenvalues and eigenvectors: $\Sigma u = \lambda u$; sort from largest
   to smallest.
4. Put the first $k$ eigenvectors in $U_k$; $z = U_k^\mathsf{T}(x - \bar{x})$.

## Formulas

| What | Formula |
|---|---|
| variance in direction $u$ | $u^\mathsf{T}\Sigma u$ |
| total variance | $\operatorname{tr}(\Sigma) = \sum\lambda_j$ |
| share of explained variance | $\frac{\lambda_j}{\sum_i\lambda_i}$ |
| component score | $z = U_k^\mathsf{T}(x - \bar{x})$ |
| reconstruction | $\hat{x} = \bar{x} + U_k z$ |
| reconstruction error (one point) | $\lVert x - \bar{x}\rVert^2 - \lVert z\rVert^2$ |
| eigenvalue from the SVD | $\lambda_j = \frac{s_j^2}{n - 1}$ |

## A 2 × 2 symmetric matrix

$\begin{pmatrix} a & b \\ b & c \end{pmatrix}$: $\lambda_1 + \lambda_2 = a + c$,
$\lambda_1\lambda_2 = ac - b^2$. If $a = c$, the eigenvectors are
$\frac{1}{\sqrt{2}}(1, 1)$ and $\frac{1}{\sqrt{2}}(1, -1)$ and the
eigenvalues $a \pm b$.

## Practical tips

- Eigenvectors must have unit length; normalise before computing scores.
- If an eigenvalue is $0$, the data lies in a lower-dimensional subspace.
- PCA does not see the target; the largest variance may not be the most
  useful direction for prediction.
