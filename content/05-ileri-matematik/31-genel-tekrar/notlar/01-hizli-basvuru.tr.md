MAT 2'nin bütün formülleri tek sayfada. Bir soruda takıldığında buraya dön; ayrıntısı ilgili bölümün başvuru notunda.

## Doğrusal cebir

| Konu | Formül |
|---|---|
| nokta çarpımı | $a \cdot b = \sum a_i b_i = \lVert a \rVert \lVert b \rVert \cos\theta$ |
| uzunluk | $\lVert a \rVert = \sqrt{a \cdot a}$ |
| matris çarpımı | $(m \times n)(n \times p) = m \times p$; $(AB)^\mathsf{T} = B^\mathsf{T}A^\mathsf{T}$ |
| $2 \times 2$ ters | $\frac{1}{ad - bc}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$ |
| ters çarpım | $(AB)^{-1} = B^{-1}A^{-1}$ |
| özdeğer | $Av = \lambda v$, $\det(A - \lambda I) = 0$; $\sum\lambda = \operatorname{iz}$, $\prod\lambda = \det$ |
| SVD | $A = USV^\mathsf{T}$ |

## Kalkülüs

| Konu | Formül |
|---|---|
| türev tanımı | $f'(x) = \lim_{h \to 0}\frac{f(x + h) - f(x)}{h}$ |
| kuvvet, üstel, log | $(x^n)' = nx^{n-1}$, $(e^x)' = e^x$, $(\ln x)' = \frac{1}{x}$ |
| çarpım, bölüm | $(fg)' = f'g + fg'$, $\left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2}$ |
| zincir | $(f(g(x)))' = f'(g(x))\,g'(x)$ |
| sigmoid | $\sigma' = \sigma(1 - \sigma)$ |
| Taylor | $f(x) \approx f(a) + f'(a)(x - a) + \frac{f''(a)}{2}(x - a)^2$ |
| integral | $\int x^n dx = \frac{x^{n+1}}{n + 1} + C$ |
| gradyan inişi | $w \leftarrow w - \eta\nabla J(w)$ |

## Olasılık

| Konu | Formül |
|---|---|
| koşullu | $P(A \mid B) = \frac{P(A \cap B)}{P(B)}$ |
| Bayes | $P(A \mid B) = \frac{P(B \mid A)P(A)}{P(B)}$ |
| beklenen değer | $E[X] = \sum x\,p(x)$; $E[aX + b] = aE[X] + b$ |
| varyans | $E[X^2] - E[X]^2$; $\operatorname{Var}(aX + b) = a^2\operatorname{Var}X$ |
| binom | $np$, $np(1 - p)$ |
| normal | yüzde $68$–$95$–$99{,}7$ kuralı; $z = \frac{x - \mu}{\sigma}$ |

## İstatistik ve kestirim

| Konu | Formül |
|---|---|
| standart hata | $\frac{\sigma}{\sqrt{n}}$; oran için $\sqrt{\frac{p(1 - p)}{n}}$ |
| güven aralığı | $\bar{x} \pm 1{,}96\,\text{SE}$ |
| kovaryans | $E[XY] - E[X]E[Y]$; $r = \frac{\operatorname{Cov}}{\sigma_X\sigma_Y}$ |
| MLE | $\hat{\theta} = \arg\max\sum\ln f(x_i \mid \theta)$ |
| regresyon | $w = (X^\mathsf{T}X)^{-1}X^\mathsf{T}y$ |
| lojistik | $p = \sigma(w^\mathsf{T}x + b)$; gradyan $(p - y)x$ |
| entropi | $H = -\sum p\log p$; $H(P, Q) = H(P) + D_{\mathrm{KL}}$ |
| PCA | $\Sigma u = \lambda u$; pay $\frac{\lambda_j}{\sum\lambda}$ |
