A worked example for each method in the lesson. Try the question yourself first, then read the solution.

## 1. The second derivative test

**Question:** Is $f(x) = x^4 + x^2$ convex?

$f''(x) = 12x^2 + 2 > 0$ everywhere: yes, even strictly convex.

## 2. A function that is not convex

**Question:** Is $f(x) = x^3$ convex?

$f''(x) = 6x$, negative for $x < 0$: no.

## 3. The chord test

**Question:** For $f(x) = x^2$, check the chord inequality with $a = 0$, $b = 4$, $t = \frac{1}{2}$.

$f(2) = 4$; the chord gives $\frac{0 + 16}{2} = 8$. $4 \le 8$ ✓.

## 4. The Hessian test

**Question:** Is $f(x, y) = x^2 + xy + y^2$ convex?

$H = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$, eigenvalues $3$ and $1$: yes.

## 5. With the rules

**Question:** Is $L(\mathbf{w}) = \sum_i (y_i - \mathbf{w} \cdot \mathbf{x}_i)^2 + \lVert \mathbf{w} \rVert^2$ convex?

Each term is a convex function ($u^2$) with a linear expression put in; $\lVert \mathbf{w} \rVert^2$ is convex too. The sum is convex.

## 6. Lagrange

**Question:** Minimise $f = x^2 + y^2$ subject to $x + 2y = 4$.

$(2x, 2y) = \lambda(1, 2)$: $x = \frac{\lambda}{2}$, $y = \lambda$. $\frac{\lambda}{2} + 2\lambda = 4$, $\lambda = \frac{8}{5}$: $\left(\frac{4}{5}, \frac{8}{5}\right)$, $f = \frac{16}{5}$.

## 7. The meaning of the multiplier

**Question:** Subject to $x + y = c$, the largest value of $xy$ is $\frac{c^2}{4}$. What is its derivative with respect to $c$ at $c = 10$? Compare with $\lambda$.

$\frac{c}{2} = 5 = \lambda$ ✓.

## 8. A local minimum

**Question:** The gradient of a convex loss is zero at $\mathbf{w}_0$. What can be said about $\mathbf{w}_0$?

It is a global minimum; there is no better point.
