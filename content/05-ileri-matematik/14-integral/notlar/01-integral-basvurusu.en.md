A short version of everything in the lesson. Come back here when you get stuck on a question.

## Definitions

| Concept | Formula |
|---|---|
| definite integral | $\int_a^b f(x) \, dx = \lim_{n \to \infty} \sum f(x_i) \Delta x$ |
| antiderivative | $\int f(x) \, dx = F(x) + C$, $F' = f$ |
| fundamental theorem | $\int_a^b f(x) \, dx = F(b) - F(a)$ |
| derivative of the area | $\dfrac{d}{dx} \int_a^x f(t) \, dt = f(x)$ |

## Table of antiderivatives

| $f(x)$ | $\int f(x) \, dx$ |
|---|---|
| $k$ (constant) | $kx + C$ |
| $x^n$, $n \neq -1$ | $\dfrac{x^{n+1}}{n + 1} + C$ |
| $\dfrac{1}{x}$ | $\ln \lvert x \rvert + C$ |
| $e^{kx}$ | $\dfrac{e^{kx}}{k} + C$ |
| $\dfrac{1}{\sqrt{x}}$ | $2\sqrt{x} + C$ |

## Properties

| Property | Formula |
|---|---|
| linearity | $\int (af + bg) = a \int f + b \int g$ |
| joining intervals | $\int_a^b f + \int_b^c f = \int_a^c f$ |
| swapping limits | $\int_b^a f = -\int_a^b f$ |
| sign | area below the axis counts as minus |

## Substitution

1. Call the inner function $u$; $du = u' \, dx$.
2. Write the integral entirely in terms of $u$.
3. In a definite integral, convert the limits to $u$ too.
4. Finish, or go back to $x$.

## Numerical integration

| Method | Formula |
|---|---|
| right-end rectangles | $h \sum_{i=1}^{n} f(x_i)$ |
| trapezoid | $\dfrac{h}{2}\big(f_0 + 2f_1 + \cdots + 2f_{n-1} + f_n\big)$ |

## Probability

| Concept | Formula |
|---|---|
| probability of an interval | $P(a \le X \le b) = \int_a^b f(x) \, dx$ |
| total | $\int_{-\infty}^{\infty} f = 1$ |
| expected value | $E[X] = \int x f(x) \, dx$ |
| average value | $\dfrac{1}{b - a} \int_a^b f(x) \, dx$ |
