A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. Sample covariance

**Question:** $x = 2, 4, 6$ and $y = 1, 3, 8$. What is $s_{xy}$?

$\bar{x} = 4$, $\bar{y} = 4$. The deviations are $-2, 0, 2$ and
$-3, -1, 4$; the products $6, 0, 8$, sum $14$. $s_{xy} = \frac{14}{2} = 7$.

## 2. Correlation

**Question:** What is $r$ for the same data?

$s_x^2 = \frac{4 + 0 + 4}{2} = 4$, $s_x = 2$.
$s_y^2 = \frac{9 + 1 + 16}{2} = 13$, $s_y \approx 3.606$.
$r = \frac{7}{2 \cdot 3.606} \approx 0.97$.

## 3. The short formula

**Question:** $E[X] = 2$, $E[Y] = 3$, $E[XY] = 7.5$. What is the
covariance?

$7.5 - 2 \cdot 3 = 1.5$.

## 4. A change of units

**Question:** The covariance between height (cm) and weight (kg) is $60$.
If height is measured in metres, what happens to the covariance and the
correlation?

Height is multiplied by $0.01$: the covariance is $0.6$. The correlation
does not change.

## 5. The variance of a sum

**Question:** $\operatorname{Var}X = 9$, $\operatorname{Var}Y = 16$,
$\operatorname{Cov}(X, Y) = 6$. What are $\operatorname{Var}(X + Y)$ and
$\operatorname{Var}(X - Y)$?

$9 + 16 + 12 = 37$ and $9 + 16 - 12 = 13$.

## 6. Covariance from correlation

**Question:** $r = -0.4$, $\sigma_X = 5$, $\sigma_Y = 10$. What is the
covariance?

$-0.4 \cdot 5 \cdot 10 = -20$.

## 7. A linear transformation

**Question:** $\operatorname{Cov}(X, Y) = 2$. What is
$\operatorname{Cov}(3X + 1, -2Y)$? What happens to the correlation?

$3 \cdot (-2) \cdot 2 = -12$. The coefficients have opposite signs: the
correlation keeps its size and flips its sign.

## 8. Zero covariance, dependent variables

**Question:** $X$ takes the values $-2, -1, 1, 2$ with equal probability;
$Y = |X|$. What is the covariance?

$E[X] = 0$. $E[XY] = \frac{-4 - 1 + 1 + 4}{4} = 0$. The covariance is $0$;
yet once $X$ is known, $Y$ is known exactly.

## 9. A covariance matrix

**Question:** $\operatorname{Var}X_1 = 1$, $\operatorname{Var}X_2 = 4$,
$\operatorname{Cov}(X_1, X_2) = 1.2$. What are the covariance matrix and
$r$?

$\Sigma = \begin{pmatrix} 1 & 1.2 \\ 1.2 & 4 \end{pmatrix}$,
$r = \frac{1.2}{1 \cdot 2} = 0.6$.

## 10. Averaging two models

**Question:** Two models have error variance $4$, and their errors have
correlation $0.5$. What is the error variance of their average?

$\frac{4 \cdot (1 + 0.5)}{2} = 3$. Better than a single model, but worse
than the $2$ with independent errors.
