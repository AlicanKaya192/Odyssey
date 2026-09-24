A short version of everything in the lesson. Come back here when you get stuck on a question.

## The rules

| Rule | Formula |
|---|---|
| power | $(x^n)' = n x^{n-1}$ |
| sum, constant multiple | $(af + bg)' = af' + bg'$ |
| product | $(fg)' = f'g + fg'$ |
| quotient | $\left(\dfrac{f}{g}\right)' = \dfrac{f'g - fg'}{g^2}$ |
| chain | $\big(f(g(x))\big)' = f'(g(x)) \cdot g'(x)$ |

## Basic derivatives

| $f(x)$ | $f'(x)$ |
|---|---|
| $e^x$ | $e^x$ |
| $e^{kx}$ | $k e^{kx}$ |
| $a^x$ | $a^x \ln a$ |
| $\ln x$ | $\dfrac{1}{x}$ |
| $\ln g(x)$ | $\dfrac{g'(x)}{g(x)}$ |
| $\sqrt{g(x)}$ | $\dfrac{g'(x)}{2\sqrt{g(x)}}$ |
| $\sigma(x)$ | $\sigma(x)\big(1 - \sigma(x)\big)$ |
| $\max(0, x)$ | $0$ ($x < 0$), $1$ ($x > 0$) |

## Applying the chain rule

1. Separate the outer and inner functions: $y = f(u)$, $u = g(x)$.
2. Differentiate the outer one, leaving the inside as it is: $f'(u)$.
3. Multiply by the derivative of the inner one: $f'(u) \cdot g'(x)$.
4. Write $g(x)$ back in place of $u$.

## Which rule?

| Expression | Rule |
|---|---|
| $x^3 e^x$ | product |
| $\dfrac{x^2}{x + 1}$ | quotient (or product + chain) |
| $(x^2 + 1)^7$ | chain |
| $e^{x^2} \ln x$ | product, with a chain inside |

## Practical tips

- Write roots and fractional powers as exponents.
- The order on top in the quotient rule: the derivative of the top first.
- For a complicated product or quotient, taking $\ln$ first (logarithmic differentiation) can make the work easier.
