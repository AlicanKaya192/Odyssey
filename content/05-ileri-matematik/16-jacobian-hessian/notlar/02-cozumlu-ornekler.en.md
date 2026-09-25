A worked example for each method in the lesson. Try the question yourself first, then read the solution.

## 1. A Jacobian

**Question:** What is the Jacobian of $F(x, y) = (xy, \ x - y^2)$?

$\begin{bmatrix} y & x \\ 1 & -2y \end{bmatrix}$.

## 2. The linear approximation

**Question:** For the same $F$, approximate $F(2.1, 1)$ around $(2, 1)$.

$F(2, 1) = (2, 1)$, $J = \begin{bmatrix} 1 & 2 \\ 1 & -2 \end{bmatrix}$, $\mathbf{h} = (0.1, 0)$: $(2.1, \ 1.1)$. (The true value is the same.)

## 3. The chain rule

**Question:** If $z = x + y^2$, $x = t^3$, $y = 2t$, what is $\frac{dz}{dt}$ at $t = 1$?

$1 \cdot 3t^2 + 2y \cdot 2 = 3 + 8 = 11$.

## 4. The Jacobian of a linear layer

**Question:** $\mathbf{z} = W\mathbf{x} + \mathbf{b}$ with $W$ of size $4 \times 3$. What size is the Jacobian?

$4 \times 3$; the Jacobian is $W$ itself.

## 5. A Hessian

**Question:** What is the Hessian of $f = x^2 y + y^3$?

$f_{xx} = 2y$, $f_{xy} = 2x$, $f_{yy} = 6y$: $\begin{bmatrix} 2y & 2x \\ 2x & 6y \end{bmatrix}$.

## 6. Classification

**Question:** What is the critical point of $f = x^2 + 4xy + y^2$ at $(0, 0)$?

$H = \begin{bmatrix} 2 & 4 \\ 4 & 2 \end{bmatrix}$, $\det H = 4 - 16 = -12 < 0$: a saddle.

## 7. With eigenvalues

**Question:** At a critical point the Hessian's eigenvalues are $3$ and $0.5$. What is the point?

Both positive: a local minimum.

## 8. The learning rate limit

**Question:** The largest eigenvalue of the loss's Hessian is $20$. Roughly what is the upper limit for a stable learning rate?

$\frac{2}{20} = 0.1$.
