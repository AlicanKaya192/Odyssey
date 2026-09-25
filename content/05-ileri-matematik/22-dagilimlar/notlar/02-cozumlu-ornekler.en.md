A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. Bernoulli

**Question:** A user clicks an ad with probability $0.2$. What are the
expected value and variance of the click variable?

$E = 0.2$, $\operatorname{Var} = 0.2 \cdot 0.8 = 0.16$.

## 2. Binomial

**Question:** A coin is tossed $5$ times. What is the probability of exactly
$2$ heads, and of at least $1$ head?

$\binom{5}{2} \cdot 0.5^5 = \frac{10}{32} = 0.3125$. At least one:
$1 - \frac{1}{32} = \frac{31}{32}$.

## 3. The binomial's expected value

**Question:** $4$ percent of parts in a production run are defective. What
are the expected number of defective parts in $100$ and its variance?

$np = 4$, $np(1 - p) = 4 \cdot 0.96 = 3.84$.

## 4. Poisson

**Question:** A call centre gets an average of $2$ calls a minute. What is
the probability of no call in a minute, and of at most $1$ call?

$P(0) = e^{-2} \approx 0.135$. $P(1) = 2e^{-2}$; at most one:
$3e^{-2} \approx 0.406$.

## 5. From binomial to Poisson

**Question:** Compare $P(X = 0)$ for the binomial with $n = 20$, $p = 0.1$
and for the Poisson with $\lambda = 2$.

Binomial $0.9^{20} \approx 0.122$, Poisson $e^{-2} \approx 0.135$. Close;
they get closer as $n$ grows and $p$ shrinks.

## 6. An exponential wait

**Question:** Customers arrive at an average rate of $0.25$ per minute. What
is the mean wait, and the probability of waiting more than $8$ minutes?

$\frac{1}{0.25} = 4$ minutes. $e^{-0.25 \cdot 8} = e^{-2} \approx 0.135$.

## 7. Memorylessness

**Question:** At the same place no customer has come for $5$ minutes. What
is the probability that none comes for at least $3$ more minutes?

Memorylessness: $P(X > 3) = e^{-0.75} \approx 0.472$; the $5$ minutes
already waited do not matter.

## 8. Normal and 68–95–99.7

**Question:** Test scores are $\mathcal{N}(100, 15^2)$. What share score
between $85$ and $115$, and above $130$?

$\mu \pm \sigma$: about $68$ percent. $130 = \mu + 2\sigma$:
$1 - 0.977 = 0.023$.

## 9. The standard normal

**Question:** In the same test, what are $P(X \leq 115)$ and
$P(X \leq 85)$?

$z = 1$: $0.841$. $z = -1$: $1 - 0.841 = 0.159$.

## 10. Uniform

**Question:** A bus comes on the hour and you arrive at the stop at a random
time; the wait is uniform on $[0, 60]$ minutes. What is the probability of
waiting less than $15$ minutes, and the mean wait?

$\frac{15}{60} = 0.25$; the mean is $30$ minutes.
