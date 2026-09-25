All the formulas of MATH 2 on one page. Come back here when you get stuck on a question; the details are in each section's reference note.

## Linear algebra

| Topic | Formula |
|---|---|
| dot product | $a \cdot b = \sum a_i b_i = \lVert a \rVert \lVert b \rVert \cos\theta$ |
| length | $\lVert a \rVert = \sqrt{a \cdot a}$ |
| matrix product | $(m \times n)(n \times p) = m \times p$; $(AB)^\mathsf{T} = B^\mathsf{T}A^\mathsf{T}$ |
| $2 \times 2$ inverse | $\frac{1}{ad - bc}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$ |
| inverse of a product | $(AB)^{-1} = B^{-1}A^{-1}$ |
| eigenvalue | $Av = \lambda v$, $\det(A - \lambda I) = 0$; $\sum\lambda = \operatorname{tr}$, $\prod\lambda = \det$ |
| SVD | $A = USV^\mathsf{T}$ |

## Calculus

| Topic | Formula |
|---|---|
| definition of the derivative | $f'(x) = \lim_{h \to 0}\frac{f(x + h) - f(x)}{h}$ |
| power, exponential, log | $(x^n)' = nx^{n-1}$, $(e^x)' = e^x$, $(\ln x)' = \frac{1}{x}$ |
| product, quotient | $(fg)' = f'g + fg'$, $\left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2}$ |
| chain | $(f(g(x)))' = f'(g(x))\,g'(x)$ |
| sigmoid | $\sigma' = \sigma(1 - \sigma)$ |
| Taylor | $f(x) \approx f(a) + f'(a)(x - a) + \frac{f''(a)}{2}(x - a)^2$ |
| integral | $\int x^n dx = \frac{x^{n+1}}{n + 1} + C$ |
| gradient descent | $w \leftarrow w - \eta\nabla J(w)$ |

## Probability

| Topic | Formula |
|---|---|
| conditional | $P(A \mid B) = \frac{P(A \cap B)}{P(B)}$ |
| Bayes | $P(A \mid B) = \frac{P(B \mid A)P(A)}{P(B)}$ |
| expected value | $E[X] = \sum x\,p(x)$; $E[aX + b] = aE[X] + b$ |
| variance | $E[X^2] - E[X]^2$; $\operatorname{Var}(aX + b) = a^2\operatorname{Var}X$ |
| binomial | $np$, $np(1 - p)$ |
| normal | the $68$–$95$–$99.7$ percent rule; $z = \frac{x - \mu}{\sigma}$ |

## Statistics and estimation

| Topic | Formula |
|---|---|
| standard error | $\frac{\sigma}{\sqrt{n}}$; for a proportion $\sqrt{\frac{p(1 - p)}{n}}$ |
| confidence interval | $\bar{x} \pm 1.96\,\text{SE}$ |
| covariance | $E[XY] - E[X]E[Y]$; $r = \frac{\operatorname{Cov}}{\sigma_X\sigma_Y}$ |
| MLE | $\hat{\theta} = \arg\max\sum\ln f(x_i \mid \theta)$ |
| regression | $w = (X^\mathsf{T}X)^{-1}X^\mathsf{T}y$ |
| logistic | $p = \sigma(w^\mathsf{T}x + b)$; gradient $(p - y)x$ |
| entropy | $H = -\sum p\log p$; $H(P, Q) = H(P) + D_{\mathrm{KL}}$ |
| PCA | $\Sigma u = \lambda u$; share $\frac{\lambda_j}{\sum\lambda}$ |
