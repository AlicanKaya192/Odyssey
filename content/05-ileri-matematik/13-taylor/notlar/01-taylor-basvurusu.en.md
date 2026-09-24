A short version of everything in the lesson. Come back here when you get stuck on a question.

## Approximations

| Degree | Formula |
|---|---|
| 1 (linear) | $f(a + h) \approx f(a) + f'(a) h$ |
| 2 | $f(a + h) \approx f(a) + f'(a) h + \dfrac{f''(a)}{2} h^2$ |
| $n$ | $P_n(x) = \sum_{k=0}^{n} \dfrac{f^{(k)}(a)}{k!} (x - a)^k$ |

$k! = 1 \cdot 2 \cdots k$, $0! = 1$: $1, 1, 2, 6, 24, 120, \ldots$

## Expansions (around x = 0)

| Function | Expansion |
|---|---|
| $e^x$ | $1 + x + \dfrac{x^2}{2} + \dfrac{x^3}{6} + \dfrac{x^4}{24} + \cdots$ |
| $\ln(1 + x)$ | $x - \dfrac{x^2}{2} + \dfrac{x^3}{3} - \dfrac{x^4}{4} + \cdots$ |
| $\dfrac{1}{1 - x}$ | $1 + x + x^2 + x^3 + \cdots$ |
| $\dfrac{1}{1 + x}$ | $1 - x + x^2 - x^3 + \cdots$ |
| $\sqrt{1 + x}$ | $1 + \dfrac{x}{2} - \dfrac{x^2}{8} + \cdots$ |
| $(1 + x)^n$ | $1 + nx + \dfrac{n(n - 1)}{2} x^2 + \cdots$ |

## Error

| Rule | Explanation |
|---|---|
| size | roughly the first term left out |
| change with $h$ | proportional to $h^{n+1}$ for degree $n$ |
| place | valid near the point where it was built |

## Machine learning

| Method | Approximation it rests on | Step |
|---|---|---|
| gradient descent | linear | $\Delta = -\eta L'(w)$ |
| Newton | quadratic | $\Delta = -\dfrac{L'(w)}{L''(w)}$ |

## Practical tips

- For roots and powers, first bring it to the form $1 + x$: $\sqrt{4.1} = 2\sqrt{1.025}$.
- To find the coefficients, compute the derivatives at $a$ and divide by $k!$.
- Newton finds the minimum of a quadratic function in a single step.
