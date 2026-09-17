The short version of everything in the lesson. Come back here when a formula or a problem stops you.

## Definition

$$
\log_b x = y \quad\Longleftrightarrow\quad b^y = x
$$

- $b > 0$ and $b \neq 1$.
- $x > 0$. **Zero and negative numbers have no logarithm.**
- $y$ can take any value: negative, zero, fractional.

## Values that are the same in every base

| Expression | Value | Reason |
|---|---|---|
| $\log_b 1$ | $0$ | $b^0 = 1$ |
| $\log_b b$ | $1$ | $b^1 = b$ |
| $\log_b b^k$ | $k$ | The definition itself |
| $b^{\log_b x}$ | $x$ | Exponent and logarithm cancel |
| $\log_b \frac{1}{b}$ | $-1$ | $b^{-1} = \frac{1}{b}$ |

## Rules

| Rule | Example |
|---|---|
| $\log_b (xy) = \log_b x + \log_b y$ | $\log_{10} 200 = \log_{10} 2 + \log_{10} 100 = 0.301 + 2$ |
| $\log_b \frac{x}{y} = \log_b x - \log_b y$ | $\ln \frac{e^5}{e^2} = 5 - 2 = 3$ |
| $\log_b x^k = k \log_b x$ | $\log_2 8^{10} = 10 \cdot 3 = 30$ |
| $\log_b \sqrt[n]{x} = \frac{1}{n} \log_b x$ | $\log_{10} \sqrt{1000} = \frac{3}{2}$ |
| $\log_b x = \dfrac{\ln x}{\ln b}$ | $\log_5 20 = \frac{2.996}{1.609} = 1.861$ |
| $\log_b \frac{1}{x} = -\log_b x$ | $\ln 0.5 = -\ln 2 = -0.693$ |

**What does not expand:** $\log (x + y)$ and $\log (x - y)$. There is no rule
for the logarithm of a sum or a difference.

## Numbers worth remembering

| | Value |
|---|---|
| $\log_{10} 2$ | $0.301$ |
| $\log_{10} 3$ | $0.477$ |
| $\ln 2$ | $0.693$ |
| $\ln 10$ | $2.303$ |
| $e$ | $2.718$ |
| $\log_2 1000$ | $\approx 10$ ($2^{10} = 1024$) |
| $\log_2 10^6$ | $\approx 20$ |
| $\log_2 10^9$ | $\approx 30$ |

## Logarithms without a calculator

Knowing $\log_{10} 2 \approx 0.301$ and $\log_{10} 3 \approx 0.477$, the rules
give you many more values:

| Wanted | Written as | Result |
|---|---|---|
| $\log_{10} 4$ | $\log_{10} 2^2 = 2 \cdot 0.301$ | $0.602$ |
| $\log_{10} 5$ | $\log_{10} \frac{10}{2} = 1 - 0.301$ | $0.699$ |
| $\log_{10} 6$ | $\log_{10} (2 \cdot 3) = 0.301 + 0.477$ | $0.778$ |
| $\log_{10} 8$ | $\log_{10} 2^3 = 3 \cdot 0.301$ | $0.903$ |
| $\log_{10} 9$ | $\log_{10} 3^2 = 2 \cdot 0.477$ | $0.954$ |
| $\log_{10} 0.004$ | $\log_{10} (4 \cdot 10^{-3}) = 0.602 - 3$ | $-2.398$ |

The last row is an important habit: write the number as **"a number times a
power of 10"**. The power of 10 gives the whole part of the logarithm, the
remaining factor gives the decimal part.

## What the sign tells you

When the base is greater than 1 ($b > 1$, which in practice it always is):

| Range of $x$ | $\log_b x$ |
|---|---|
| $0 < x < 1$ | negative |
| $x = 1$ | $0$ |
| $x > 1$ | positive |
| $x \to 0$ | goes to $-\infty$ |

Probabilities lie between $0$ and $1$; their logarithms are always negative.
The minus sign in loss formulas turns this positive.

As the base grows, the logarithm of a number above 1 **gets smaller**:
$\log_2 10 \approx 3.32$ but $\log_3 10 \approx 2.10$. A larger base reaches the
same number with a smaller exponent.

## Types of equation and their methods

| Equation | Method |
|---|---|
| $b^{f(x)} = b^{g(x)}$ (same base) | Set the exponents equal: $f(x) = g(x)$. No logarithm needed. |
| $a \cdot b^{x} = c$ | Divide: $b^x = \frac{c}{a}$, then $x = \frac{\ln (c/a)}{\ln b}$ |
| $b^{f(x)} = d^{g(x)}$ (different bases) | Take $\ln$ of both sides, bring the exponents down, solve the linear equation |
| $\log_b f(x) = k$ | Rewrite with the definition: $f(x) = b^k$ |
| $\log_b f(x) + \log_b g(x) = k$ | Combine: $f(x)\,g(x) = b^k$ |
| $\log_b f(x) = \log_b g(x)$ | Set the insides equal: $f(x) = g(x)$ |

**The last step is the same in every logarithmic equation:** put every value
you find into every logarithm of the original equation and check that it is
positive.
