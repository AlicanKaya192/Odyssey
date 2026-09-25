A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. Centring

**Question:** The points are $(1, 2)$, $(3, 4)$, $(5, 9)$. What are they
after centring?

The mean is $(3, 5)$. Centred: $(-2, -3)$, $(0, -1)$, $(2, 4)$.

## 2. The variance in a direction

**Question:** $\Sigma = \begin{pmatrix} 4 & 1 \\ 1 & 2 \end{pmatrix}$. What are
the variances in the directions $u = (1, 0)$ and $u = (0, 1)$?

$u^\mathsf{T}\Sigma u$: $4$ and $2$; the diagonal entries, the features' own
variances.

## 3. Eigenvalues and eigenvectors

**Question:** $\Sigma = \begin{pmatrix} 3 & 1 \\ 1 & 3 \end{pmatrix}$. What are
the eigenvalues and eigenvectors?

$a = c = 3$, $b = 1$: eigenvalues $4$ and $2$; eigenvectors
$\frac{1}{\sqrt{2}}(1, 1)$ and $\frac{1}{\sqrt{2}}(1, -1)$.

## 4. Explained variance

**Question:** For the same matrix, what is the 1st component's share?

$\frac{4}{4 + 2} \approx 0.667$.

## 5. Total variance

**Question:** With three features the diagonal of the covariance matrix is
$2$, $1$, $3$. What is the total variance?

The trace: $6$. The eigenvalues also sum to $6$.

## 6. A component score

**Question:** $u_1 = (0.6, \ 0.8)$, $x - \bar{x} = (5, 5)$. What is $z_1$?

$0.6 \cdot 5 + 0.8 \cdot 5 = 7$.

## 7. Reconstruction

**Question:** $\bar{x} = (1, 1)$, $z_1 = 7$, $u_1 = (0.6, \ 0.8)$. What is
$\hat{x}$?

$(1, 1) + 7 \cdot (0.6, \ 0.8) = (5.2, \ 6.6)$.

## 8. Reconstruction error

**Question:** For the same point, what is the squared error?

$\lVert(5, 5)\rVert^2 - z_1^2 = 50 - 49 = 1$.

## 9. How many components?

**Question:** The eigenvalues are $5, 3, 1, 1$. How many components for $90$
percent?

The cumulative shares are $0.5$, $0.8$, $0.9$: $3$ components.

## 10. Eigenvalues from the SVD

**Question:** The largest singular value of centred data with $n = 6$
observations is $10$. What is the largest eigenvalue?

$\frac{10^2}{6 - 1} = 20$.
