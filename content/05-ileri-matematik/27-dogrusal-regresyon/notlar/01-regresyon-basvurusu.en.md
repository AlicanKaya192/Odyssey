A short version of everything in the lesson. Come back here when you get stuck on a question.

## One feature

| What | Formula |
|---|---|
| model | $\hat{y} = b + wx$ |
| slope | $w = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2} = r\frac{s_y}{s_x}$ |
| intercept | $b = \bar{y} - w\bar{x}$ |
| model without intercept | $w = \frac{\sum x_i y_i}{\sum x_i^2}$ |

## Matrix form

| What | Formula |
|---|---|
| loss | $\text{SSE} = \lVert y - Xw \rVert^2$ |
| gradient | $-2X^\mathsf{T}(y - Xw)$ |
| normal equations | $X^\mathsf{T}Xw = X^\mathsf{T}y$ |
| solution | $w = (X^\mathsf{T}X)^{-1}X^\mathsf{T}y$ |
| ridge | $w = (X^\mathsf{T}X + \lambda I)^{-1}X^\mathsf{T}y$ |

$2 \times 2$ inverse: $\begin{pmatrix} a & b \\ c & d \end{pmatrix}^{-1} =
\frac{1}{ad - bc}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$.

## Fit

| What | Formula |
|---|---|
| residual | $e_i = y_i - \hat{y}_i$, $\sum e_i = 0$ |
| SST | $\sum (y_i - \bar{y})^2$ |
| $R^2$ | $1 - \frac{\text{SSE}}{\text{SST}}$ ($r^2$ with one feature) |
| noise variance | MLE $\frac{\text{SSE}}{n}$, unbiased $\frac{\text{SSE}}{n - d - 1}$ |

## Practical tips

- Do not forget the column of $1$s at the front of $X$.
- The line passes through $(\bar{x}, \bar{y})$; use it as a check.
- The residuals are perpendicular to every column: $X^\mathsf{T}e = 0$.
- If the determinant of $X^\mathsf{T}X$ is near zero there is
  multicollinearity; try ridge.
