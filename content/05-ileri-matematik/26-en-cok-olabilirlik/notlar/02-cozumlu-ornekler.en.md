A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. The MLE of a proportion

**Question:** $6$ heads in $20$ tosses. What is $\hat{p}$?

$\hat{p} = \frac{6}{20} = 0.3$.

## 2. Comparing two likelihoods

**Question:** $7$ heads in $10$ tosses. How many times $L(0.5)$ is
$L(0.7)$?

$L(0.7) = 0.7^7 \cdot 0.3^3 \approx 0.00222$,
$L(0.5) = 0.5^{10} \approx 0.000977$. The ratio is $\approx 2.28$.

## 3. A log-likelihood value

**Question:** What is $\ell(0.7)$ for the same data?

$7\ln 0.7 + 3\ln 0.3 \approx 7(-0.357) + 3(-1.204) \approx -6.11$.

## 4. The normal distribution

**Question:** The data is $2, 4, 9$. What are $\hat{\mu}$ and
$\hat{\sigma}^2$?

$\hat{\mu} = 5$. The squared deviations are $9, 1, 16$;
$\hat{\sigma}^2 = \frac{26}{3} \approx 8.67$. (The unbiased estimate is
$\frac{26}{2} = 13$.)

## 5. Poisson

**Question:** Daily error counts are $2, 0, 3, 1, 4$. What is
$\hat{\lambda}$?

$\hat{\lambda} = \bar{x} = \frac{10}{5} = 2$.

## 6. The exponential distribution

**Question:** Waiting times are $2, 3, 5$ minutes. What is
$\hat{\lambda}$?

$\bar{x} = \frac{10}{3}$, $\hat{\lambda} = \frac{3}{10} = 0.3$ (per
minute).

## 7. Why the logarithm?

**Question:** What is the joint probability of $1000$ independent events of
probability $0.1$, and its logarithm?

$0.1^{1000} = 10^{-1000}$: a computer makes this $0$. Its logarithm is
$1000 \ln 0.1 \approx -2302.6$: a perfectly usable number.

## 8. Squared error and the NLL

**Question:** $y_i = \hat{y}_i + \varepsilon_i$, $\varepsilon_i \sim
\mathcal{N}(0, \sigma^2)$. What is the NLL proportional to?

$-\ell = \frac{n}{2}\ln(2\pi\sigma^2) + \frac{1}{2\sigma^2}\sum (y_i -
\hat{y}_i)^2$; with $\sigma$ fixed, it is smallest where the sum of squared
errors is smallest.

## 9. The Laplace correction

**Question:** $3$ heads in $3$ tosses. What are the MLE and the Laplace
estimate?

MLE $\frac{3}{3} = 1$. Laplace $\frac{3 + 1}{3 + 2} = 0.8$.

## 10. A categorical distribution

**Question:** A die was rolled $10$ times: $1$ twice, $2$ three times, $3$
once, $4$ never, $5$ twice, $6$ twice. What are $\hat{p}_4$ and
$\hat{p}_2$?

$\hat{p}_k = \frac{n_k}{n}$: $\hat{p}_4 = 0$, $\hat{p}_2 = 0.3$. With little
data an estimate of $0$ is not reliable.
