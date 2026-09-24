A worked example for each method in the lesson. Try the question yourself first, then read the solution.

## 1. The linear approximation

**Question:** Approximate $\sqrt{9.2}$ with the tangent at $a = 9$.

$f(9) = 3$, $f'(9) = \frac{1}{6}$: $3 + \frac{0.2}{6} \approx 3.0333$ (the true value is $3.0332$).

## 2. The power shortcut

**Question:** About how much is $0.98^5$?

$(1 - 0.02)^5 \approx 1 - 5 \cdot 0.02 = 0.9$ (the true value is $0.9039$).

## 3. Second degree

**Question:** Find $e^{0.1}$ with the second degree approximation.

$1 + 0.1 + 0.005 = 1.105$ (the true value is $1.10517$).

## 4. A Taylor coefficient

**Question:** What is the coefficient of $x^3$ in the Maclaurin expansion of $f(x) = e^{2x}$?

$f'''(0) = 8$; $\frac{8}{3!} = \frac{4}{3}$.

## 5. A logarithm

**Question:** Approximate $\ln 0.9$ with two terms.

$x = -0.1$: $-0.1 - \frac{0.01}{2} = -0.105$ (the true value is $-0.10536$).

## 6. At another point

**Question:** What is the second degree Taylor polynomial of $f(x) = x^3$ around $a = 1$?

$f(1) = 1$, $f'(1) = 3$, $f''(1) = 6$: $1 + 3(x - 1) + 3(x - 1)^2$.

## 7. Estimating the error

**Question:** About how large is the error of the approximation $e^{0.2} \approx 1 + 0.2$?

The first term left out is $\frac{0.2^2}{2} = 0.02$ (the true error is $0.0214$).

## 8. A Newton step

**Question:** For $L(w) = (w - 3)^2$, where does one Newton step from $w = 0$ go?

$L'(0) = -6$, $L''(0) = 2$: $0 - \frac{-6}{2} = 3$. For a quadratic function, the minimum in a single step.
