A worked example for each method in the lesson. Try the question yourself first, then read the solution.

## 1. A diagonal matrix

**Question:** What are the singular values of $\begin{bmatrix} 3 & 0 \\ 0 & -2 \end{bmatrix}$?

A diagonal matrix already stretches along the axes: $x$ by 3, $y$ by $-2$
(by 2, flipped). Singular values cannot be negative; the sign goes into
$U$ as a reflection. The singular values are $3$ and $2$.

With $A^\mathsf{T}A = \begin{bmatrix} 9 & 0 \\ 0 & 4 \end{bmatrix}$ too: the
eigenvalues are $9, 4$ and their square roots $3, 2$ ✓.

## 2. A full SVD

**Question:** Find the SVD of $A = \begin{bmatrix} 2 & 2 \\ -1 & 1 \end{bmatrix}$.

$$
A^\mathsf{T}A = \begin{bmatrix} 2 & -1 \\ 2 & 1 \end{bmatrix} \begin{bmatrix} 2 & 2 \\ -1 & 1 \end{bmatrix} = \begin{bmatrix} 5 & 3 \\ 3 & 5 \end{bmatrix}
$$

Trace $10$, determinant $16$: the eigenvalues are $8$ and $2$. The
singular values are $\sigma_1 = 2\sqrt{2} \approx 2.83$ and $\sigma_2 =
\sqrt{2} \approx 1.41$.

Eigenvectors: for $\lambda = 8$, $y = x$; for $\lambda = 2$, $y = -x$.

$$
\mathbf{v}_1 = \tfrac{1}{\sqrt{2}}(1, 1)
\qquad
\mathbf{v}_2 = \tfrac{1}{\sqrt{2}}(1, -1)
$$

$A\mathbf{v}_1 = \tfrac{1}{\sqrt{2}}(4, 0)$; dividing by $\sigma_1$ gives $\mathbf{u}_1 = (1, 0)$.
$A\mathbf{v}_2 = \tfrac{1}{\sqrt{2}}(0, -2)$; dividing by $\sigma_2$ gives $\mathbf{u}_2 = (0, -1)$.

Check: $\sigma_1\sigma_2 = 2\sqrt{2} \cdot \sqrt{2} = 4 = |\det A| = |2 + 2|$ ✓.

## 3. A rectangular matrix

**Question:** What are the singular values and the rank of $A = \begin{bmatrix} 1 & 1 \\ 1 & 1 \\ 0 & 0 \end{bmatrix}$?

$A$ is $3 \times 2$; $A^\mathsf{T}A$ is $2 \times 2$:

$$
A^\mathsf{T}A = \begin{bmatrix} 2 & 2 \\ 2 & 2 \end{bmatrix}
$$

The eigenvalues are $4$ and $0$ (trace 4, determinant 0). The singular
values are $2$ and $0$: rank $1$. Indeed the two columns are the same.

## 4. A rank-1 matrix

**Question:** What is the SVD of $A = \begin{bmatrix} 2 & 4 \\ 1 & 2 \end{bmatrix}$?

Every row is a multiple of $(1, 2)$: $A = \begin{bmatrix} 2 \\ 1 \end{bmatrix} \begin{bmatrix} 1 & 2 \end{bmatrix}$.
There is a single layer:

$$
\sigma_1 = \|(2, 1)\| \cdot \|(1, 2)\| = \sqrt{5} \cdot \sqrt{5} = 5
$$

$\mathbf{u}_1 = \tfrac{1}{\sqrt{5}}(2, 1)$, $\mathbf{v}_1 = \tfrac{1}{\sqrt{5}}(1, 2)$, $\sigma_2 = 0$.

Check: the sum of the squares of the entries is $4 + 16 + 1 + 4 = 25 = \sigma_1^2$ ✓.

## 5. The energy share

**Question:** A matrix has singular values $20, 10, 5, 2, 1$. How much of
the energy do the rank-2 and rank-3 approximations keep?

Squares: $400, 100, 25, 4, 1$; total $530$.

- Rank 2: $\dfrac{400 + 100}{530} = \dfrac{500}{530} \approx 0.943$, that is 94.3%.
- Rank 3: $\dfrac{525}{530} \approx 0.991$, that is 99.1%.

The error of the rank-3 approximation is $\sqrt{4 + 1} = \sqrt{5} \approx 2.24$.

## 6. The condition number

**Question:** A square matrix has largest singular value $100$ and smallest $0.01$. What is its condition number?

$$
\frac{\sigma_1}{\sigma_n} = \frac{100}{0.01} = 10\,000
$$

The matrix is invertible but "nearly singular": a small error in the input
can grow up to $10\,000$ times in the solution.

## 7. Storage

**Question:** For a $256 \times 256$ greyscale image, how many numbers does the rank-20 approximation store?

$$
20 \cdot (256 + 256 + 1) = 20 \cdot 513 = 10\,260
$$

The original takes $256 \cdot 256 = 65\,536$ numbers; the approximation about 15.7% of that.
