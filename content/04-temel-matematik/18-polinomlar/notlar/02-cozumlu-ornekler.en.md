A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. Degree and leading coefficient

**Question:** What are the degree, the leading coefficient and the constant
term of $5 + 3x - x^4 + 2x^2$?

Put it in standard form: $-x^4 + 2x^2 + 3x + 5$. Degree $4$, leading
coefficient $-1$, constant term $5$. The leading coefficient belongs to the
largest power, not to the term written first.

## 2. Evaluating

**Question:** For $P(x) = x^3 - 3x + 1$, what is $P(-2)$?

$(-2)^3 = -8$ and $-3 \cdot (-2) = 6$: $P(-2) = -8 + 6 + 1 = -1$. Putting a
negative number in brackets prevents sign mistakes.

## 3. Subtracting

**Question:** What is $(4x^3 - x + 2) - (x^3 + 2x^2 - 3x + 5)$?

Every sign in the second bracket flips: $4x^3 - x + 2 - x^3 - 2x^2 + 3x - 5$.
Like terms: $3x^3 - 2x^2 + 2x - 3$.

## 4. Multiplying

**Question:** What is $(x + 3)(x^2 - 2x + 4)$?

$$
\begin{aligned}
&x^3 - 2x^2 + 4x + 3x^2 - 6x + 12 \\
&= x^3 + x^2 - 2x + 12
\end{aligned}
$$

Check: for $x = 1$ the left side is $4 \cdot 3 = 12$ and the right side
$1 + 1 - 2 + 12 = 12$ ✓.

## 5. Synthetic division

**Question:** What are the quotient and the remainder of
$(x^3 - 8) \div (x - 2)$?

Make room for the missing terms: coefficients $1, 0, 0, -8$, $a = 2$.

| | $1$ | $0$ | $0$ | $-8$ |
|---|---|---|---|---|
| $a = 2$ | | $2$ | $4$ | $8$ |
| result | $1$ | $2$ | $4$ | $0$ |

Quotient $x^2 + 2x + 4$, remainder $0$: $x^3 - 8 = (x - 2)(x^2 + 2x + 4)$.
This is the difference of cubes identity.

## 6. The remainder theorem

**Question:** What is the remainder when $P(x) = x^4 - 3x^2 + 5$ is divided
by $(x + 1)$?

$(x + 1) = (x - (-1))$, so $a = -1$. $P(-1) = 1 - 3 + 5 = 3$. No division
needed.

## 7. An unknown coefficient

**Question:** If $x^3 + ax - 6$ is divisible by $(x - 2)$, what is $a$?

Divisible means the remainder is $0$, that is $P(2) = 0$:
$8 + 2a - 6 = 0$, so $a = -1$.

## 8. Finding the roots

**Question:** Factor $x^3 - 7x + 6$.

The candidates are the divisors of $6$. $P(1) = 1 - 7 + 6 = 0$, so
$(x - 1)$ is a factor. Synthetic division ($1, 0, -7, 6$ with $a = 1$)
gives the quotient $x^2 + x - 6$. $x^2 + x - 6 = (x + 3)(x - 2)$:

$$
x^3 - 7x + 6 = (x - 1)(x + 3)(x - 2)
$$

The roots are $-3$, $1$, $2$.

## 9. End behaviour

**Question:** Where do the ends of the graph of $-2x^5 + x$ go?

Degree $5$ (odd), leading coefficient $-2$ (negative): the left end goes
up, the right end down. Because the degree is odd it has at least one real
root; here $x = 0$ is one.
