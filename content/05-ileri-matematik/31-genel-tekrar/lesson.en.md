# Overall Review

MATH 2 ends here. You started with vectors; with matrices, eigenvalues and
the SVD you saw data as a geometric object. With limits, derivatives,
gradients and backpropagation you worked out how a model learns. With
probability, distributions, sampling and estimation you measured
uncertainty; and at the end you saw the three branches meet in
regression, logistic regression, entropy and PCA. This section teaches no
new topic: it shows how the pieces connect, uses them all together in one
problem and collects the most common traps in one list. The quiz and
problems are mixed from the whole module.

## How do the pieces connect?

MATH 2 advances along three branches, and all three meet in machine
learning.

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Vectors</b><br>dot product, length</span>
    <span class="arrow">→</span>
    <span class="node"><b>Matrices</b><br>product, inverse, systems</span>
    <span class="arrow">→</span>
    <span class="node"><b>Eigenvalues and SVD</b><br>the skeleton of a matrix</span>
  </div>
  <figcaption>The linear algebra branch: data is a matrix, a model is a matrix product, and the shape of the data is in the eigenvectors.</figcaption>
</figure>

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Limits and derivatives</b><br>rate of change</span>
    <span class="arrow">→</span>
    <span class="node"><b>Gradient</b><br>multivariable slope</span>
    <span class="arrow">→</span>
    <span class="node"><b>Gradient descent</b><br>step by step to the minimum</span>
    <span class="arrow">→</span>
    <span class="node"><b>Backpropagation</b><br>the chain rule layer by layer</span>
  </div>
  <figcaption>The calculus branch: a model learns by computing the gradient of the loss and stepping the other way.</figcaption>
</figure>

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Probability</b><br>conditional, Bayes</span>
    <span class="arrow">→</span>
    <span class="node"><b>Distributions</b><br>expected value, variance</span>
    <span class="arrow">→</span>
    <span class="node"><b>Sampling</b><br>standard error, tests</span>
    <span class="arrow">→</span>
    <span class="node"><b>Estimation</b><br>MLE, loss functions</span>
  </div>
  <figcaption>The probability and statistics branch: loss functions are born from likelihood; the reliability of results is measured through sampling.</figcaption>
</figure>

The last sections join the three branches: in linear regression the
normal equations (algebra), the loss and its gradient (calculus) and
normal noise (probability) give the same solution; PCA is the
eigenvectors of the covariance matrix; cross-entropy is both information
theory and likelihood.

## One problem from start to finish

Picture an engineer working on a recommendation and classification
system. The questions come in turn from different corners of MATH 2.

### 1. Similarity: vectors

Two users' ratings of three films are $a = (4, 0, 3)$ and $b = (3, 1, 4)$.
The dot product is $12 + 0 + 12 = 24$; the lengths are
$\lVert a \rVert = 5$, $\lVert b \rVert = \sqrt{26} \approx 5.10$.

$$
\cos\theta = \frac{a \cdot b}{\lVert a \rVert \lVert b \rVert} \approx \frac{24}{25.50} \approx 0.94
$$

Their tastes are very similar; recommending one's favourite film to the
other makes sense.

### 2. Model and loss: the derivative

A simple model $\hat{y} = wx$; data $x = (1, 2, 3)$, $y = (1, 3, 5)$. The
loss is $J(w) = \sum (y_i - wx_i)^2$ and its derivative:

$$
J'(w) = -2\sum x_i y_i + 2w\sum x_i^2 = -44 + 28w
$$

The point where the derivative is zero is $w^* = \frac{22}{14} \approx
1.57$; this is the one-dimensional form of the normal equations,
$w = \frac{\sum xy}{\sum x^2}$.

### 3. Learning: gradient descent

If the data were very large we would go step by step instead of using the
formula: $w \leftarrow w - \eta J'(w)$, $\eta = 0.01$. From $w_0 = 0$,
$w_1 = 0.44$, $w_2 \approx 0.76$, $w_3 \approx 0.98$…

<figure class="fig">
<svg viewBox="0 0 420 262" width="420"><line class="grid" x1="50.0" y1="226.0" x2="50.0" y2="26.0"/><line class="grid" x1="78.3" y1="226.0" x2="78.3" y2="26.0"/><line class="grid" x1="106.7" y1="226.0" x2="106.7" y2="26.0"/><line class="grid" x1="135.0" y1="226.0" x2="135.0" y2="26.0"/><line class="grid" x1="163.3" y1="226.0" x2="163.3" y2="26.0"/><line class="grid" x1="191.7" y1="226.0" x2="191.7" y2="26.0"/><line class="grid" x1="220.0" y1="226.0" x2="220.0" y2="26.0"/><line class="grid" x1="248.3" y1="226.0" x2="248.3" y2="26.0"/><line class="grid" x1="276.7" y1="226.0" x2="276.7" y2="26.0"/><line class="grid" x1="305.0" y1="226.0" x2="305.0" y2="26.0"/><line class="grid" x1="333.3" y1="226.0" x2="333.3" y2="26.0"/><line class="grid" x1="361.7" y1="226.0" x2="361.7" y2="26.0"/><line class="grid" x1="390.0" y1="226.0" x2="390.0" y2="26.0"/><line class="grid" x1="50.0" y1="226.0" x2="390.0" y2="226.0"/><line class="grid" x1="50.0" y1="201.0" x2="390.0" y2="201.0"/><line class="grid" x1="50.0" y1="176.0" x2="390.0" y2="176.0"/><line class="grid" x1="50.0" y1="151.0" x2="390.0" y2="151.0"/><line class="grid" x1="50.0" y1="126.0" x2="390.0" y2="126.0"/><line class="grid" x1="50.0" y1="101.0" x2="390.0" y2="101.0"/><line class="grid" x1="50.0" y1="76.0" x2="390.0" y2="76.0"/><line class="grid" x1="50.0" y1="51.0" x2="390.0" y2="51.0"/><line class="grid" x1="50.0" y1="26.0" x2="390.0" y2="26.0"/><line class="line" x1="50.0" y1="226.0" x2="390.0" y2="226.0"/><polyline class="curve" fill="none" points="61.3,23.6 62.8,26.0 64.2,28.3 65.6,30.6 67.0,33.0 68.4,35.3 69.8,37.5 71.2,39.8 72.7,42.1 74.1,44.3 75.5,46.6 76.9,48.8 78.3,51.0 79.8,53.2 81.2,55.4 82.6,57.5 84.0,59.7 85.4,61.8 86.8,63.9 88.2,66.1 89.7,68.2 91.1,70.2 92.5,72.3 93.9,74.4 95.3,76.4 96.8,78.4 98.2,80.4 99.6,82.4 101.0,84.4 102.4,86.4 103.8,88.3 105.2,90.3 106.7,92.2 108.1,94.1 109.5,96.0 110.9,97.9 112.3,99.8 113.8,101.6 115.2,103.5 116.6,105.3 118.0,107.1 119.4,108.9 120.8,110.7 122.3,112.5 123.7,114.2 125.1,116.0 126.5,117.7 127.9,119.4 129.3,121.1 130.8,122.8 132.2,124.5 133.6,126.2 135.0,127.8 136.4,129.4 137.8,131.1 139.2,132.7 140.7,134.2 142.1,135.8 143.5,137.4 144.9,138.9 146.3,140.5 147.8,142.0 149.2,143.5 150.6,145.0 152.0,146.5 153.4,147.9 154.8,149.4 156.2,150.8 157.7,152.2 159.1,153.7 160.5,155.1 161.9,156.4 163.3,157.8 164.8,159.2 166.2,160.5 167.6,161.8 169.0,163.1 170.4,164.4 171.8,165.7 173.2,167.0 174.7,168.2 176.1,169.5 177.5,170.7 178.9,171.9 180.3,173.1 181.8,174.3 183.2,175.5 184.6,176.6 186.0,177.8 187.4,178.9 188.8,180.0 190.2,181.1 191.7,182.2 193.1,183.3 194.5,184.3 195.9,185.4 197.3,186.4 198.7,187.4 200.2,188.4 201.6,189.4 203.0,190.4 204.4,191.4 205.8,192.3 207.2,193.2 208.7,194.2 210.1,195.1 211.5,195.9 212.9,196.8 214.3,197.7 215.8,198.5 217.2,199.4 218.6,200.2 220.0,201.0 221.4,201.8 222.8,202.6 224.2,203.3 225.7,204.1 227.1,204.8 228.5,205.5 229.9,206.3 231.3,207.0 232.8,207.6 234.2,208.3 235.6,209.0 237.0,209.6 238.4,210.2 239.8,210.8 241.2,211.4 242.7,212.0 244.1,212.6 245.5,213.1 246.9,213.7 248.3,214.2 249.8,214.7 251.2,215.2 252.6,215.7 254.0,216.2 255.4,216.6 256.8,217.1 258.2,217.5 259.7,217.9 261.1,218.3 262.5,218.7 263.9,219.1 265.3,219.4 266.8,219.8 268.2,220.1 269.6,220.4 271.0,220.7 272.4,221.0 273.8,221.3 275.2,221.6 276.7,221.8 278.1,222.0 279.5,222.3 280.9,222.5 282.3,222.6 283.8,222.8 285.2,223.0 286.6,223.1 288.0,223.3 289.4,223.4 290.8,223.5 292.2,223.6 293.7,223.7 295.1,223.7 296.5,223.8 297.9,223.8 299.3,223.8 300.8,223.9 302.2,223.9 303.6,223.8 305.0,223.8 306.4,223.8 307.8,223.7 309.2,223.6 310.7,223.5 312.1,223.4 313.5,223.3 314.9,223.2 316.3,223.0 317.8,222.9 319.2,222.7 320.6,222.5 322.0,222.3 323.4,222.1 324.8,221.9 326.2,221.6 327.7,221.4 329.1,221.1 330.5,220.8 331.9,220.5 333.3,220.2 334.8,219.9 336.2,219.5 337.6,219.2 339.0,218.8 340.4,218.4 341.8,218.0 343.2,217.6 344.7,217.2 346.1,216.8 347.5,216.3 348.9,215.8 350.3,215.4 351.8,214.9 353.2,214.3 354.6,213.8 356.0,213.3 357.4,212.7 358.8,212.2 360.2,211.6 361.7,211.0 363.1,210.4 364.5,209.8 365.9,209.1 367.3,208.5 368.8,207.8 370.2,207.1 371.6,206.5 373.0,205.8 374.4,205.0 375.8,204.3 377.2,203.6 378.7,202.8 380.1,202.0 381.5,201.2 382.9,200.4 384.3,199.6 385.8,198.8 387.2,197.9 388.6,197.1 390.0,196.2"/><line class="curve2" x1="78.3" y1="51.0" x2="136.9" y2="129.1"/><polygon class="dot2" points="140.7,134.2 133.7,130.3 138.9,126.4"/><line class="curve2" x1="140.7" y1="134.2" x2="180.9" y2="173.0"/><polygon class="dot2" points="185.5,177.4 178.0,174.7 182.5,170.0"/><line class="curve2" x1="185.5" y1="177.4" x2="212.6" y2="196.2"/><polygon class="dot2" points="217.9,199.8 210.0,198.3 213.7,193.0"/><line class="curve2" x1="217.9" y1="199.8" x2="235.4" y2="208.5"/><polygon class="dot2" points="241.1,211.4 233.1,211.1 236.0,205.2"/><line class="curve2" x1="241.1" y1="211.4" x2="251.9" y2="215.2"/><polygon class="dot2" points="257.9,217.4 249.9,218.0 252.1,211.9"/><line class="curve2" x1="257.9" y1="217.4" x2="263.7" y2="218.9"/><polygon class="dot2" points="269.9,220.5 262.0,221.8 263.6,215.5"/><circle class="dot2" cx="78.3" cy="51.0" r="3.6"/><circle class="dot2" cx="140.7" cy="134.2" r="3.6"/><circle class="dot2" cx="185.5" cy="177.4" r="3.6"/><circle class="dot2" cx="217.9" cy="199.8" r="3.6"/><circle class="dot2" cx="241.1" cy="211.4" r="3.6"/><circle class="dot2" cx="257.9" cy="217.4" r="3.6"/><circle class="dot2" cx="269.9" cy="220.5" r="3.6"/><line class="curve3" stroke-dasharray="5 4" x1="301.0" y1="226.0" x2="301.0" y2="223.9"/><circle class="dot3" cx="301.0" cy="223.9" r="4.5"/><text class="ink" x="86.3" y="55.0" font-size="10" text-anchor="start">w₀ = 0</text><text class="ink" x="148.7" y="138.2" font-size="10" text-anchor="start">w₁ = 0.44</text><text class="ink" x="301.0" y="240.0" font-size="10" text-anchor="middle">w* ≈ 1.57</text><text class="ink" x="382.9" y="166.0" font-size="11" text-anchor="end">J(w) = Σ(y − wx)²</text><text class="dim" x="248.3" y="66.0" font-size="10" text-anchor="middle">the error shrinks by 0.72 at each step</text><text class="dim" x="78.3" y="240.0" font-size="9" text-anchor="middle">0.0</text><text class="dim" x="149.2" y="240.0" font-size="9" text-anchor="middle">0.5</text><text class="dim" x="220.0" y="240.0" font-size="9" text-anchor="middle">1.0</text><text class="dim" x="361.7" y="240.0" font-size="9" text-anchor="middle">2.0</text><text class="dim" x="390.0" y="254.0" font-size="10" text-anchor="end">w</text></svg>
  <figcaption>Gradient descent on the loss parabola. Each step brings the distance to the minimum down to 0.72 of what it was; the steps get shorter because the slope flattens.</figcaption>
</figure>

### 4. Classification: logistic regression

Another model gives the probability that an email is spam as
$p = \sigma(2x - 3)$. For $x = 2$, $p = \sigma(1) \approx 0.731$. If the
email really is spam ($y = 1$), the log-loss is $-\ln 0.731 \approx
0.313$; the gradient of the weight is $(p - y)x \approx -0.269 \cdot 2
\approx -0.538$: the weight will be increased.

### 5. How reliable is the decision: Bayes

$20$ percent of emails are spam. The model flags $90$ percent of spam and
$5$ percent of normal emails as "spam". $P(\text{flag}) = 0.18 + 0.04 =
0.22$ and

$$
P(\text{spam} \mid \text{flag}) = \frac{0.18}{0.22} \approx 0.82
$$

About one in five flagged emails is actually normal.

### 6. Evaluation: a confidence interval

The model scored $85$ percent accuracy on $400$ test emails.
$\text{SE} = \sqrt{\frac{0.85 \cdot 0.15}{400}} \approx 0.018$; the $95$
percent confidence interval is $0.85 \pm 0.035$, that is about
$[0.815, \ 0.885]$. Another model's $86$ percent lies inside this
interval: telling them apart needs more test data.

### 7. Compressing features: PCA

The covariance matrix of two features is $\begin{pmatrix} 5 & 4 \\ 4 & 5
\end{pmatrix}$. The eigenvalues are $9$ and $1$: a single component
carries $90$ percent of the variance, so using one instead of two features
may be enough.

In seven steps vectors, the derivative, gradient descent, the sigmoid and
log-loss, Bayes, a confidence interval and eigenvalues worked together.
The mathematics of a machine learning system is made of exactly these
pieces.

## What did you learn, section by section?

| Topic | Key idea | In machine learning |
|---|---|---|
| Vectors, dot product | length, angle, cosine similarity | similarity search |
| Matrices and multiplication | the size rule, transformations | layers $Wx + b$ |
| Determinant, inverse, systems | Gaussian elimination, rank | normal equations |
| Eigenvalues and SVD | $Av = \lambda v$, $A = USV^\mathsf{T}$ | PCA, compression |
| Limits and continuity | approaching | the basis of the derivative |
| Derivatives and their rules | slope, the chain rule | backpropagation |
| Applications of derivatives | $f' = 0$, the second derivative | the minimum of a loss |
| Taylor | local polynomial approximation | optimisation |
| Integrals | area, accumulation | probability density |
| Gradient, Jacobian, Hessian | steepest direction, curvature | training many parameters |
| Convexity, gradient descent | $w \leftarrow w - \eta\nabla J$ | the training loop |
| Backpropagation | the chain rule layer by layer | neural networks |
| Conditional probability, Bayes | $P(A \mid B)$, prior and posterior | spam filters, diagnosis |
| Random variables, distributions | $E$, $\operatorname{Var}$, binomial, normal | modelling |
| Sampling, tests | $\text{SE} = \frac{\sigma}{\sqrt{n}}$, p-value | A/B tests |
| Covariance, correlation | varying together | multicollinearity |
| Maximum likelihood | the parameter that makes the data most probable | loss functions |
| Linear and logistic regression | $X^\mathsf{T}Xw = X^\mathsf{T}y$; sigmoid, log-loss | basic models |
| Entropy, cross-entropy, KL | information and extra bits | classification loss |
| PCA | eigenvectors of the covariance | dimensionality reduction |

## The most common traps

| Trap | Correct |
|---|---|
| $AB = BA$ | matrix multiplication is generally not commutative |
| $(AB)^{-1} = A^{-1}B^{-1}$ | $B^{-1}A^{-1}$ |
| $\det(A + B) = \det A + \det B$ | the determinant does not distribute over addition |
| $\frac{d}{dx}f(g(x)) = f'(g(x))$ | do not forget $\times\, g'(x)$ |
| zero derivative, so a minimum | it may be a maximum or a saddle |
| a large learning rate is always faster | it may diverge |
| $P(A \mid B) = P(B \mid A)$ | turned round with Bayes |
| $\operatorname{Var}(X + Y) = \operatorname{Var}X + \operatorname{Var}Y$ always | $+ 2\operatorname{Cov}(X, Y)$ |
| $\text{SE} = \frac{\sigma}{n}$ | $\frac{\sigma}{\sqrt{n}}$ |
| the p-value is the probability of $H_0$ | it is a probability about the data |
| correlation is causation | an experiment is needed |
| KL is symmetric | $D(P \parallel Q) \neq D(Q \parallel P)$ |
| not centring before PCA | subtract the mean first |

## The next step

With MATH 2 the mathematical foundation of AI is complete. From here:

- **The Machine Learning path:** see how every formula you derived here is
  used in code; linear and logistic regression, decision trees,
  clustering and dimensionality reduction.
- **Write it yourself:** implementing gradient descent, logistic
  regression or PCA with nothing but NumPy is the best way to make the
  mathematics stick.
- **Deep learning:** neural networks are backpropagation at large scale;
  matrix multiplication, the chain rule, softmax and cross-entropy appear
  on every line.

## Summary

- The three branches of MATH 2: linear algebra (the language of data and
  models), calculus (the mechanism of learning), probability and
  statistics (uncertainty and loss).
- In a real problem the three work together: similarity is measured with
  vectors, learning with gradients, decisions with probability,
  reliability with sampling.
- Regression, logistic regression, entropy and PCA are where the three
  branches cross.
- The most common mistakes come from operations wrongly assumed to
  commute, the forgotten chain factor, the reversed conditional
  probability and mixing up the square root and $n$.
