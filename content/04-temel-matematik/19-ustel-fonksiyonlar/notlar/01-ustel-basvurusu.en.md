A short version of everything in the lesson. Come back here when you get stuck on a question.

## Linear or exponential?

| | Linear | Exponential |
|---|---|---|
| form | $a + mx$ | $a \cdot b^x$ |
| at each step | add $m$ | multiply by $b$ |
| what is constant | consecutive differences | consecutive ratios |
| in the long run | slow | overtakes every line |

## The exponential function

$f(x) = a \cdot b^x$, $a \neq 0$, $b > 0$, $b \neq 1$.

| Property | For $b^x$ |
|---|---|
| $f(0)$ | $1$ ($a$ in general) |
| domain | all real numbers |
| range | $y > 0$ |
| asymptote | $y = 0$ |
| $b > 1$ | increasing |
| $0 < b < 1$ | decreasing |

$\left( \frac{1}{b} \right)^x = b^{-x}$: mirror image in the $y$-axis.
$b^x + k$: asymptote $y = k$.

## Formulas

| Situation | Formula |
|---|---|
| growth by $r$ percent | $A_0 (1 + r)^t$ |
| decay by $r$ percent | $A_0 (1 - r)^t$ |
| doubling time $T$ | $N_0 \cdot 2^{t / T}$ |
| half-life $h$ | $N_0 \cdot \left( \frac{1}{2} \right)^{t / h}$ |
| interest $n$ times a year | $A_0 \left( 1 + \frac{r}{n} \right)^{nt}$ |
| continuous growth | $A_0 \, e^{rt}$ |

$e \approx 2.71828$. Rule of 72: at $r$ percent, doubling in about
$\frac{72}{r}$ periods.

## Exponential equations

Bring to the same base, set the exponents equal: $4^x = 8$ ⇒
$2^{2x} = 2^3$ ⇒ $x = \frac{3}{2}$. No common base: logarithms.

## In machine learning

| Where | Formula |
|---|---|
| sigmoid | $\sigma(z) = \dfrac{1}{1 + e^{-z}}$, $\sigma(0) = 0.5$ |
| softmax | $p_i = \dfrac{e^{z_i}}{\sum_j e^{z_j}}$ |
| learning rate decay | $\eta_0 \cdot c^t$, $0 < c < 1$ |
| gradients | $0.9^{100} \approx 0$, $1.1^{100} \approx 13{,}781$ |

## Practical tips

- For decay the factor is $1 - r$: a $20$ percent decrease is $0.8$.
- Percentages do not add up, they multiply.
- If a time is given, the exponent is $\frac{t}{T}$ or $\frac{t}{h}$.
- Do not mix up $2^x$ and $x^2$: is the exponent varying, or the base?
