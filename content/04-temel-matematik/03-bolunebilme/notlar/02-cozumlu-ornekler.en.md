A worked example for each method in the lesson. Try the question yourself first, then read the solution.

## 1. Using the divisibility rules together

**Question:** Which of $2, 3, 4, 6, 9$ divide $7\,452$?

- $2$: the last digit is $2$, even ✓
- $3$ and $9$: $7 + 4 + 5 + 2 = 18$; $18$ is a multiple of both $3$ and $9$ ✓ ✓
- $4$: the last two digits give $52 = 4 \cdot 13$ ✓
- $6$: because it is divisible by $2$ and $3$ ✓

All five divide it.

## 2. A primality test

**Question:** Is $91$ prime?

Since $10 \cdot 10 = 100 > 91$, checking $2, 3, 5, 7$ is enough. $2$: odd.
$3$: $9 + 1 = 10$, no. $5$: last digit $1$, no. $7$: $7 \cdot 13 = 91$.
**Not prime.**

## 3. Prime factorisation

**Question:** Write $504$ as a product of primes.

Divide by small primes in turn:

$$
504 \xrightarrow{\div 2} 252 \xrightarrow{\div 2} 126 \xrightarrow{\div 2} 63 \xrightarrow{\div 3} 21 \xrightarrow{\div 3} 7
$$

$$
504 = 2^3 \cdot 3^2 \cdot 7
$$

## 4. The number of divisors

**Question:** How many divisors does $504$ have?

The exponents are $3, 2, 1$: $(3 + 1)(2 + 1)(1 + 1) = 24$.

## 5. GCD and LCM with prime factors

**Question:** What are $\text{GCD}(60, 72)$ and $\text{LCM}(60, 72)$?

$$
60 = 2^2 \cdot 3 \cdot 5, \qquad 72 = 2^3 \cdot 3^2
$$

GCD: the common primes are $2$ and $3$, smaller exponents: $2^2 \cdot 3 = 12$.

LCM: all primes, larger exponents: $2^3 \cdot 3^2 \cdot 5 = 360$.

Check: $12 \cdot 360 = 4\,320 = 60 \cdot 72$ ✓.

## 6. Euclid's algorithm

**Question:** What is $\text{GCD}(252, 198)$?

$$
\begin{aligned}
252 &= 198 \cdot 1 + 54 \\
198 &= 54 \cdot 3 + 36 \\
54 &= 36 \cdot 1 + 18 \\
36 &= 18 \cdot 2 + 0
\end{aligned}
$$

The GCD is $18$.

## 7. A GCD problem

**Question:** Two rods, $48$ cm and $80$ cm long, are to be cut into the
longest possible equal pieces with nothing left over. How long is each
piece, and how many pieces are there in total?

The piece length must divide both and be as large as possible:
$\text{GCD}(48, 80) = 16$ cm. The number of pieces is $48 \div 16 + 80
\div 16 = 3 + 5 = 8$.

## 8. An LCM problem

**Question:** Three lamps flash every $4$, $6$ and $10$ seconds. After
flashing together, how many seconds pass before they flash together
again?

$4 = 2^2$, $6 = 2 \cdot 3$, $10 = 2 \cdot 5$. The LCM is $2^2 \cdot 3
\cdot 5 = 60$ seconds.
