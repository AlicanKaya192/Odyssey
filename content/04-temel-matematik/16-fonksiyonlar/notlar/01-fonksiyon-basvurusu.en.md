The short version of everything in the lesson. Come back here when you get stuck on a question.

## Basic ideas

| Idea | Meaning |
|---|---|
| $f(x)$ | the rule $f$ applied to $x$ |
| domain | the accepted inputs |
| range | the outputs that can come out |
| graph | the points $(x, f(x))$ |
| function condition | one output for each input (vertical line test) |

## Finding the domain

| Expression | Condition |
|---|---|
| $\dfrac{p(x)}{q(x)}$ | $q(x) \neq 0$ |
| $\sqrt{g(x)}$ | $g(x) \ge 0$ |
| polynomial | no condition |

## Composition and inverse

| Operation | How |
|---|---|
| $(g \circ f)(x) = g(f(x))$ | first $f$, then give its output to $g$ |
| $f^{-1}$ | write $y = f(x)$, get $x$ out, swap the letters |
| check | $f(f^{-1}(x)) = x$ and $f^{-1}(f(x)) = x$ |

## Basic graphs

| Function | Shape | Range |
|---|---|---|
| $ax + b$ | line | all numbers ($a \neq 0$) |
| $x^2$ | parabola | $y \ge 0$ |
| $\lvert x \rvert$ | V | $y \ge 0$ |
| $\sqrt{x}$ | half curve | $y \ge 0$ |
| $\dfrac{1}{x}$ | two-branched curve | $y \neq 0$ |

## Practical tips

- When substituting, replace **every** $x$ with the input in brackets.
- In a composition, work from the inside out.
- $f^{-1}(x)$ and $\dfrac{1}{f(x)}$ are different things.
- ReLU: $\max(0, x)$; sigmoid: $\dfrac{1}{1 + e^{-x}}$, output between $0$ and $1$.
