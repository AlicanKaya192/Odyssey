A short version of everything in the lesson. Come back here when you get stuck on a question.

## Definitions

| Concept | Definition |
|---|---|
| convex set | the segment joining two points stays in the set |
| convex function | $f(ta + (1 - t)b) \le t f(a) + (1 - t) f(b)$ |
| concave | $-f$ is convex |
| strictly convex | the chord strictly above; the minimiser is unique |

## Tests

| Situation | Condition for convexity (everywhere) |
|---|---|
| one variable | $f''(x) \ge 0$ |
| several variables | Hessian positive semidefinite: eigenvalues $\ge 0$ |
| $2 \times 2$ Hessian | $f_{xx} \ge 0$, $f_{yy} \ge 0$, $\det H \ge 0$ |
| tangent | $f(y) \ge f(x) + \nabla f(x) \cdot (y - x)$ |

## Convex building blocks

| Function | Convex? |
|---|---|
| $x^2$, $\lvert x \rvert$, $e^x$, $\max(0, x)$ | yes |
| $-\ln x$, $x \ln x$ ($x > 0$) | yes |
| $\ln x$, $\sqrt{x}$ | no (concave) |
| $ax + b$ | both convex and concave |
| $x^3$ | no |

## Operations that preserve it

- Sums with non-negative coefficients.
- Composition with a linear expression: $f(A\mathbf{x} + \mathbf{b})$.
- Taking the maximum: $\max(f_1, f_2)$.

## Lagrange

| Step | What to do |
|---|---|
| 1 | write the equations $\nabla f = \lambda \nabla g$ |
| 2 | add the constraint $g = c$ |
| 3 | solve the system; compare the candidates' values |

$\lambda$: the approximate change in the best value if the constraint is loosened by one unit.

## Machine learning

| Loss | Convex? |
|---|---|
| linear regression (MSE) | yes |
| logistic regression (log loss) | yes |
| neural network | no |
| + L2 penalty | makes it strictly convex |
