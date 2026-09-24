A worked example for each method in the lesson. Try the question yourself first, then read the solution.

## 1. Is it an eigenvector?

**Question:** For $A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}$, are $(1, -1)$ and $(1, 1)$ eigenvectors?

$$
A \begin{bmatrix} 1 \\ -1 \end{bmatrix} = \begin{bmatrix} 3 - 1 \\ -2 \end{bmatrix} = \begin{bmatrix} 2 \\ -2 \end{bmatrix} = 2 \begin{bmatrix} 1 \\ -1 \end{bmatrix}
$$

Yes, with eigenvalue $2$.

$$
A \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 4 \\ 2 \end{bmatrix}
$$

$(4, 2)$ is not a multiple of $(1, 1)$: not an eigenvector.

## 2. Eigenvalues and eigenvectors

**Question:** What are the eigenvalues and eigenvectors of $A = \begin{bmatrix} 1 & 2 \\ 2 & 1 \end{bmatrix}$?

$\operatorname{tr} A = 2$, $\det A = 1 - 4 = -3$:

$$
\lambda^2 - 2\lambda - 3 = (\lambda - 3)(\lambda + 1) = 0
$$

$\lambda = 3$ and $\lambda = -1$.

- $\lambda = 3$: $A - 3I = \begin{bmatrix} -2 & 2 \\ 2 & -2 \end{bmatrix}$, $y = x$, $\mathbf{v} = (1, 1)$.
- $\lambda = -1$: $A + I = \begin{bmatrix} 2 & 2 \\ 2 & 2 \end{bmatrix}$, $y = -x$, $\mathbf{v} = (1, -1)$.

A negative eigenvalue: vectors along $(1, -1)$ are flipped.

## 3. A triangular matrix

**Question:** What are the eigenvalues, trace and determinant of $\begin{bmatrix} 5 & 2 & 1 \\ 0 & -1 & 3 \\ 0 & 0 & 2 \end{bmatrix}$?

A triangular matrix: the eigenvalues are the diagonal, $5, -1, 2$. Check:
$\operatorname{tr} = 5 - 1 + 2 = 6$ and $\det = 5 \cdot (-1) \cdot 2 = -10$;
the same as the sum and product of the eigenvalues.

## 4. Eigenvectors of a non-symmetric matrix

**Question:** Find the eigenvectors of $A = \begin{bmatrix} 6 & -2 \\ 2 & 1 \end{bmatrix}$.

$\operatorname{tr} = 7$, $\det = 6 + 4 = 10$: the two numbers with sum 7
and product 10 are $2$ and $5$.

- $\lambda = 2$: $A - 2I = \begin{bmatrix} 4 & -2 \\ 2 & -1 \end{bmatrix}$, $2x - y = 0$, $\mathbf{v} = (1, 2)$.
- $\lambda = 5$: $A - 5I = \begin{bmatrix} 1 & -2 \\ 2 & -4 \end{bmatrix}$, $x = 2y$, $\mathbf{v} = (2, 1)$.

Check: $A(1, 2) = (6 - 4,\ 2 + 2) = (2, 4)$ ✓; $A(2, 1) = (12 - 2,\ 4 + 1) = (10, 5)$ ✓.
The eigenvectors are not perpendicular ($1 \cdot 2 + 2 \cdot 1 = 4$): the matrix is not symmetric.

## 5. Powers through eigenvectors

**Question:** For $A$ from example 2, what is $A^3\,(1, 0)$?

Split $(1, 0)$ into eigenvectors: $(1, 0) = \tfrac{1}{2}(1, 1) + \tfrac{1}{2}(1, -1)$.

$$
A^3 \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \tfrac{1}{2} \cdot 3^3 \begin{bmatrix} 1 \\ 1 \end{bmatrix} + \tfrac{1}{2} \cdot (-1)^3 \begin{bmatrix} 1 \\ -1 \end{bmatrix} = \begin{bmatrix} 13.5 - 0.5 \\ 13.5 + 0.5 \end{bmatrix} = \begin{bmatrix} 13 \\ 14 \end{bmatrix}
$$

Direct check: $A^2 = \begin{bmatrix} 5 & 4 \\ 4 & 5 \end{bmatrix}$,
$A^3 = \begin{bmatrix} 13 & 14 \\ 14 & 13 \end{bmatrix}$; column 1 is $(13, 14)$ ✓.

## 6. Eigenvalues from the rules

**Question:** The eigenvalues of $A$ are $2$ and $5$. What are the eigenvalues of $A^{-1}$, $A^2$ and $A + 2I$?

- $A^{-1}$: $\tfrac{1}{2}$ and $\tfrac{1}{5}$
- $A^2$: $4$ and $25$
- $A + 2I$: $4$ and $7$

In all three the eigenvectors are the same as those of $A$.

## 7. The long run of a Markov chain

**Question:** Each month a customer buys brand A or brand B. Someone who
bought A buys A next month with probability 80%, someone who bought B with
probability 30%. In the long run, what share of customers buys A?

$$
M = \begin{bmatrix} 0.8 & 0.3 \\ 0.2 & 0.7 \end{bmatrix}
$$

$M\mathbf{p} = \mathbf{p}$: $(M - I)\mathbf{p} = \mathbf{0}$, the first row
says $-0.2x + 0.3y = 0$, so $x = 1.5y$. The eigenvector is $(3, 2)$;
making its sum 1 gives $(0.6, 0.4)$. In the long run 60% of customers buy A.

The other eigenvalue is $0.8 + 0.7 - 1 = 0.5$: the effect of the starting
point halves every month.
