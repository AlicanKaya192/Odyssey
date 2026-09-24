The short version of everything in the lesson. Come back here when you get stuck on a question.

## Places

| Place | Value | Example ($3.752$) |
|---|---|---|
| ones | $1$ | $3$ |
| tenths | $\dfrac{1}{10}$ | $7$ |
| hundredths | $\dfrac{1}{100}$ | $5$ |
| thousandths | $\dfrac{1}{1\,000}$ | $2$ |

Programming uses a decimal point (`3.75`); many languages write a comma ($3{,}75$).

## Common conversions

| Fraction | Decimal |
|---|---|
| $\dfrac{1}{2}$ | $0.5$ |
| $\dfrac{1}{4}$ | $0.25$ |
| $\dfrac{3}{4}$ | $0.75$ |
| $\dfrac{1}{5}$ | $0.2$ |
| $\dfrac{1}{8}$ | $0.125$ |
| $\dfrac{1}{3}$ | $0.\overline{3}$ |
| $\dfrac{2}{3}$ | $0.\overline{6}$ |
| $\dfrac{1}{9}$ | $0.\overline{1}$ |

## Terminating or repeating?

If the denominator of the fraction in simplest form has only the prime
factors $2$ and $5$, the decimal ends; if it has any other prime factor,
it repeats.

**Repeating → fraction:** if $x = 0.\overline{ab}$, then $100x - x = ab$,
so $x = \dfrac{ab}{99}$. With one repeating digit, use $10x - x$ and
denominator $9$.

## Operations

| Operation | Rule |
|---|---|
| Addition, subtraction | line up the points |
| Multiplication | multiply as whole numbers; add up the places after the point |
| Division | move both points by the same amount until the divisor is whole |
| $\cdot 10^k$ | point $k$ places to the right |
| $\div 10^k$ | point $k$ places to the left |

## Rounding

The digit to the right of the rounding place:

- $0$–$4$ → round down (the digit stays)
- $5$–$9$ → round up (the digit goes up by $1$, carrying if needed)

Round once, at the end.

## Practical tips

- When comparing, equalise the places by adding zeros on the right.
- Check a product roughly: $3.75 \cdot 0.4 \approx 4 \cdot 0.4 = 1.6$.
- Multiplying by a number less than $1$ makes smaller; dividing makes larger.
- On a computer, compare decimals not with `==` but by whether their difference is tiny.
