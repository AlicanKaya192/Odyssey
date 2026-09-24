The short version of everything in the lesson. Come back here when you get stuck on a question.

## Definition

$$
A\mathbf{v} = \lambda\mathbf{v}, \qquad \mathbf{v} \ne \mathbf{0}
$$

| $\lambda$ | What happens to the eigenvector? |
|---|---|
| $\lambda > 1$ | it grows in the same direction |
| $0 < \lambda < 1$ | it shrinks in the same direction |
| $\lambda = 1$ | it does not change |
| $\lambda < 0$ | it flips (on the same line) |
| $\lambda = 0$ | it goes to zero (in the null space) |

## Computation

1. Eigenvalues: $\det(A - \lambda I) = 0$.
2. $2 \times 2$: $\lambda^2 - (\operatorname{tr} A)\,\lambda + \det A = 0$.
3. For each $\lambda$, $(A - \lambda I)\mathbf{v} = \mathbf{0}$; one row is enough, pick a solution.
4. Check: is $A\mathbf{v} = \lambda\mathbf{v}$?

## Rules

| Rule | Result |
|---|---|
| $\sum \lambda_i$ | $\operatorname{tr} A$ |
| $\prod \lambda_i$ | $\det A$ |
| Triangular / diagonal matrix | eigenvalues = the diagonal |
| $A^k$ | $\lambda^k$, same eigenvectors |
| $A^{-1}$ | $1 / \lambda$, same eigenvectors |
| $A + cI$ | $\lambda + c$, same eigenvectors |
| $cA$ | $c\lambda$ |
| $A^\mathsf{T}$ | the same eigenvalues |
| $\det A = 0$ | $0$ is an eigenvalue |

## Special matrices

| Matrix | Eigenvalues |
|---|---|
| $I$ | all $1$ |
| $\begin{bmatrix} s_1 & 0 \\ 0 & s_2 \end{bmatrix}$ | $s_1, s_2$ (eigenvectors $\mathbf{e}_1, \mathbf{e}_2$) |
| $90°$ rotation | no real eigenvalues ($\pm i$) |
| Reflection in the $x$-axis | $1$ ($\mathbf{e}_1$) and $-1$ ($\mathbf{e}_2$) |
| Projection onto the $x$-axis | $1$ and $0$ |
| Markov transition matrix | $1$ is always an eigenvalue |

## Diagonalisation

$$
A = P D P^{-1}, \qquad A^k = P D^k P^{-1}
$$

The columns of $P$ are the eigenvectors, the diagonal of $D$ the
eigenvalues (in the same order). This needs $n$ independent eigenvectors.

Shortcut: if $\mathbf{x} = c_1\mathbf{v}_1 + c_2\mathbf{v}_2$, then
$A^k\mathbf{x} = c_1\lambda_1^k\mathbf{v}_1 + c_2\lambda_2^k\mathbf{v}_2$.

## Symmetric matrix (A^ᵀ = A)

- The eigenvalues are real.
- Eigenvectors of different eigenvalues are perpendicular.
- $A = Q\Lambda Q^\mathsf{T}$, $Q^{-1} = Q^\mathsf{T}$.

## The long run

- If $|\lambda_1|$ is largest, the direction of $A^k\mathbf{x}$ approaches $\mathbf{v}_1$ (the power method).
- Markov: the stationary distribution is $M\mathbf{p} = \mathbf{p}$ (eigenvalue 1); scale so that the components add up to 1.

## Practical tips

- For $2 \times 2$, first look for two numbers whose sum is the trace and product the determinant.
- When looking for an eigenvector, **one** row of $(A - \lambda I)$ is enough; the second gives the same information.
- If only $\mathbf{0}$ comes out, the eigenvalue is wrong.
- For a triangular matrix, do not calculate; read the diagonal.
