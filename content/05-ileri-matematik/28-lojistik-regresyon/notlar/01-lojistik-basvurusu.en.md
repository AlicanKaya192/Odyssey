A short version of everything in the lesson. Come back here when you get stuck on a question.

## The model

| What | Formula |
|---|---|
| score | $z = w^\mathsf{T}x + b$ |
| sigmoid | $p = \sigma(z) = \frac{1}{1 + e^{-z}}$ |
| odds | $\frac{p}{1 - p} = e^{z}$ |
| log-odds | $\ln\frac{p}{1 - p} = z$ |
| effect of a coefficient | odds $\times\, e^{w_j}$ |
| decision boundary | $w^\mathsf{T}x + b = 0$ |

## A few sigmoid values

| $z$ | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
|---|---|---|---|---|---|---|---|
| $\sigma(z)$ | $0.047$ | $0.119$ | $0.269$ | $0.5$ | $0.731$ | $0.881$ | $0.953$ |

$\sigma(-z) = 1 - \sigma(z)$, $\ \sigma'(z) = \sigma(z)(1 - \sigma(z))$.

## Loss and gradient

| What | Formula |
|---|---|
| log-loss (one example) | $-[y\ln p + (1 - y)\ln(1 - p)]$ |
| derivative with respect to $z$ | $p - y$ |
| gradient with respect to $w$ | $(p - y)\,x$ |
| gradient descent | $w \leftarrow w - \eta\sum_i (p_i - y_i)x_i$ |
| softmax | $p_k = \frac{e^{z_k}}{\sum_j e^{z_j}}$ |
| cross-entropy | $-\ln p_{\text{correct}}$; gradient $p_k - y_k$ |

## Practical tips

- For $y = 1$ the loss is $-\ln p$, for $y = 0$ it is $-\ln(1 - p)$.
- You can also compute log-loss from the product: $-\ln\prod(\text{probability of the correct class})$.
- In softmax, adding the same constant to every score does not change the result.
- With separable data the weights grow; add regularisation.
