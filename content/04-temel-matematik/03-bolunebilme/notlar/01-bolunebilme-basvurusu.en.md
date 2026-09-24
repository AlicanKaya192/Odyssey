The short version of everything in the lesson. Come back here when you get stuck on a question.

## Divisors and multiples

If $b = a \cdot k$, then $a$ is a divisor of $b$ and $b$ a multiple of
$a$. Look for divisors in pairs: for $36$, $1 \cdot 36$, $2 \cdot 18$,
$3 \cdot 12$, $4 \cdot 9$, $6 \cdot 6$.

## Divisibility rules

| Divisor | Look at |
|---|---|
| $2$ | last digit even |
| $3$ | digit sum a multiple of $3$ |
| $4$ | last two digits a multiple of $4$ |
| $5$ | last digit $0$ or $5$ |
| $6$ | the rules for $2$ and $3$ together |
| $8$ | last three digits a multiple of $8$ |
| $9$ | digit sum a multiple of $9$ |
| $10$ | last digit $0$ |
| $11$ | alternating sum from the right ($+,-,+,-$) a multiple of $11$ |

## Primes

- Exactly two divisors: $1$ and itself.
- Up to $100$: $2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97$.
- $1$ is not prime; $2$ is the only even prime.
- Primality test: divide by the primes $p$ with $p \cdot p \le n$.

## Prime factors

$$
n = p_1^{a_1} \cdot p_2^{a_2} \cdots p_k^{a_k}
$$

The factorisation is unique. The number of divisors:

$$
(a_1 + 1)(a_2 + 1) \cdots (a_k + 1)
$$

## GCD and LCM

| | GCD | LCM |
|---|---|---|
| With prime factors | common primes, **smaller** exponents | all primes, **larger** exponents |
| Limit | cannot exceed the numbers | cannot be less than the numbers |
| Question type | split, share, largest piece | line up, same moment again |

$$
\text{GCD}(a, b) \cdot \text{LCM}(a, b) = a \cdot b
$$

**Euclid:** divide the larger by the smaller, then carry on with the
divisor and the remainder; when the remainder is $0$, the last divisor is
the GCD.

## Practical tips

- When factorising, start with small primes: divide by $2$, then $3$, then $5$.
- For two coprime numbers, the GCD is $1$ and the LCM is their product.
- If one number divides the other, the GCD is the smaller and the LCM the larger.
- Check your answer: the GCD must divide both numbers, and the LCM must be divisible by both.
