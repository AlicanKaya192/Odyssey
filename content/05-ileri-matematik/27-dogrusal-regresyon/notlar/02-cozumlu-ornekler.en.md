A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. Slope and intercept

**Question:** $\bar{x} = 4$, $\bar{y} = 10$, $s_{xy} = 6$, $s_x^2 = 3$. What
is the line?

$w = \frac{6}{3} = 2$, $b = 10 - 2 \cdot 4 = 2$: $\hat{y} = 2 + 2x$.

## 2. Slope from correlation

**Question:** $r = 0.5$, $s_y = 10$, $s_x = 2$. What is the slope?

$w = 0.5 \cdot \frac{10}{2} = 2.5$.

## 3. Residuals and SSE

**Question:** $\hat{y} = 1 + 2x$; data $(1, 3)$, $(2, 6)$, $(3, 7)$. What is
the SSE?

Predictions $3, 5, 7$; residuals $0, 1, 0$; $\text{SSE} = 1$.

## 4. R²

**Question:** $\text{SSE} = 20$, $\text{SST} = 80$. What is $R^2$?

$1 - \frac{20}{80} = 0.75$.

## 5. r from R²

**Question:** In a single-feature regression $R^2 = 0.81$ and the slope is
negative. What is $r$?

$r = -\sqrt{0.81} = -0.9$.

## 6. The normal equations

**Question:** $x = 1, 2, 3$, $y = 2, 4, 5$; a model with intercept. What is
$w$?

$X^\mathsf{T}X = \begin{pmatrix} 3 & 6 \\ 6 & 14 \end{pmatrix}$,
$X^\mathsf{T}y = \begin{pmatrix} 11 \\ 25 \end{pmatrix}$, determinant $6$.

$$
w = \frac{1}{6}\begin{pmatrix} 14 \cdot 11 - 6 \cdot 25 \\ -6 \cdot 11 + 3 \cdot 25 \end{pmatrix} = \frac{1}{6}\begin{pmatrix} 4 \\ 9 \end{pmatrix}
$$

Intercept $\approx 0.667$, slope $1.5$.

## 7. A model without intercept

**Question:** $x = 1, 2$, $y = 2, 5$; $\hat{y} = wx$. What is $w$?

$\frac{\sum xy}{\sum x^2} = \frac{2 + 10}{1 + 4} = 2.4$.

## 8. Checking perpendicularity

**Question:** For $x = 1, 2, 3$ the residuals came out $0.2$, $-0.4$,
$0.2$. Is this consistent with a least squares solution?

$\sum e = 0$ and $\sum x e = 0.2 - 0.8 + 0.6 = 0$: perpendicular to both
columns, consistent.

## 9. Ridge

**Question:** No intercept, $\sum x^2 = 5$, $\sum xy = 10$. What are least
squares and ridge with $\lambda = 5$?

Least squares $\frac{10}{5} = 2$; ridge $\frac{10}{5 + 5} = 1$.

## 10. The noise variance

**Question:** $n = 8$ observations, $1$ feature plus intercept,
$\text{SSE} = 12$. What are the MLE and the unbiased estimate of
$\sigma^2$?

MLE $\frac{12}{8} = 1.5$; unbiased $\frac{12}{8 - 2} = 2$.
