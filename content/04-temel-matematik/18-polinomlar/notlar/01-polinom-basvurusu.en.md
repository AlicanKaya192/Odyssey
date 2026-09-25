A short version of everything in the lesson. Come back here when you get stuck on a question.

## The parts

$P(x) = a_n x^n + \dots + a_1 x + a_0$

| Name | What | $3x^4 - 2x^2 + x - 5$ |
|---|---|---|
| degree | the largest power | $4$ |
| leading coefficient | $a_n$ | $3$ |
| constant term | $a_0 = P(0)$ | $-5$ |
| sum of coefficients | $P(1)$ | $-3$ |

The powers are only $0, 1, 2, \dots$; $\frac{1}{x}$ and $\sqrt{x}$ are not
polynomials.

## Operations

| Operation | Rule |
|---|---|
| adding, subtracting | like terms; subtracting flips every sign |
| multiplying | every term with every term; $x^m \cdot x^n = x^{m+n}$ |
| degree of a product | the sum of the degrees |
| degree of a sum | at most the larger one |

## Division

$$
P(x) = D(x) \cdot Q(x) + R(x), \qquad \deg R < \deg D
$$

- Long division: divide the leading term, multiply back by the divisor,
  subtract, repeat.
- Write $0$ coefficients for missing terms.
- Synthetic division: divisor $(x - a)$; bring the first coefficient down,
  multiply by $a$, add to the next. The last number is the remainder.

## Two theorems

| Theorem | What it says |
|---|---|
| remainder | the remainder on division by $(x - a)$ is $P(a)$ |
| factor | $P(a) = 0 \iff (x - a)$ is a factor |

For $(x + 3)$, $a = -3$.

## Roots and the graph

- Degree $n$ means at most $n$ real roots.
- Integer root candidates: the divisors of the constant term (if the
  leading coefficient is $1$). In general $\pm \frac{p}{q}$: $p$ divides the
  constant term, $q$ the leading coefficient.
- Odd degree: the ends point opposite ways, so at least one root is
  certain.
- Even degree: the ends point the same way.
- Single root: the curve crosses. Double root: it touches and turns back.

## Practical tips

- Put it in standard form first: read the degree and the leading
  coefficient only after that.
- If only the remainder is asked, do not divide; compute $P(a)$.
- Once you find a root, divide by $(x - a)$ and factor the quadratic that
  is left.
- Check the result by plugging in a number: $x = 1$ or $x = 0$ are the
  easiest.
