A short version of everything in the lesson. Come back here when you get stuck on a question.

## Definitions

| Concept | Formula | Geometry |
|---|---|---|
| average rate of change | $\dfrac{f(b) - f(a)}{b - a}$ | slope of the secant |
| derivative | $f'(x) = \lim_{h \to 0} \dfrac{f(x + h) - f(x)}{h}$ | slope of the tangent |
| tangent line | $y - f(a) = f'(a)(x - a)$ | the line that fits the point best |

Notations: $f'(x)$, $\dfrac{df}{dx}$, $\dfrac{dy}{dx}$, $y'$.

## Differentiating from the definition

1. Expand $f(x + h)$.
2. Subtract $f(x)$; the terms without $h$ disappear.
3. Divide by $h$ (cancel).
4. Let $h \to 0$.

## Basic derivatives

| $f(x)$ | $f'(x)$ |
|---|---|
| $c$ | $0$ |
| $x^n$ | $n x^{n-1}$ |
| $\dfrac{1}{x}$ | $-\dfrac{1}{x^2}$ |
| $\sqrt{x}$ | $\dfrac{1}{2\sqrt{x}}$ |
| $e^x$ | $e^x$ |
| $\ln x$ | $\dfrac{1}{x}$ |
| $a f(x) + b g(x)$ | $a f'(x) + b g'(x)$ |

## The sign of the derivative

| $f'(a)$ | Meaning |
|---|---|
| $> 0$ | increasing |
| $< 0$ | decreasing |
| $= 0$ | horizontal tangent: peak, valley or flat |

## Where there is no derivative

| Situation | Example |
|---|---|
| a corner | $\lvert x \rvert$, ReLU; at $x = 0$ |
| a discontinuity | the step function |
| a vertical tangent | $\sqrt[3]{x}$ at $x = 0$ |

## Numerical derivatives

| Method | Formula | Error |
|---|---|---|
| forward difference | $\dfrac{f(x + h) - f(x)}{h}$ | proportional to $h$ |
| central difference | $\dfrac{f(x + h) - f(x - h)}{2h}$ | proportional to $h^2$ |

## The learning step

$w \leftarrow w - \eta \, L'(w)$: if the slope is positive $w$ goes down, if negative it goes up.
