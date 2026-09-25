A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. A missing probability

**Question:** $p(0) = 0.2$, $p(1) = 0.5$, $p(2) = c$. What are $c$ and
$E[X]$?

The total is $1$: $c = 0.3$. $E[X] = 0 + 0.5 + 0.6 = 1.1$.

## 2. Expectation and variance

**Question:** $X$ takes the values $1, 2, 3$ with probabilities $0.2$,
$0.5$, $0.3$. What are $E[X]$, $\operatorname{Var}(X)$ and $\sigma$?

$E[X] = 0.2 + 1 + 0.9 = 2.1$. $E[X^2] = 0.2 + 2 + 2.7 = 4.9$.
$\operatorname{Var}(X) = 4.9 - 4.41 = 0.49$, $\sigma = 0.7$.

## 3. A fair game

**Question:** You pay $5$ and toss a coin twice; if both are heads you win
$20$. Is the game fair?

$E[\text{gain}] = 20 \cdot \frac{1}{4} - 5 = 0$. The expected net gain is
$0$: fair.

## 4. Linearity

**Question:** For the $X$ of the second example, what are $E[3X + 2]$ and
$\operatorname{Var}(3X + 2)$?

$3 \cdot 2.1 + 2 = 8.3$. $9 \cdot 0.49 = 4.41$; the $+2$ does not change
the variance.

## 5. The sum of two dice

**Question:** What are the expected value and variance of the sum of two
dice?

$E = 3.5 + 3.5 = 7$. The dice are independent: $\operatorname{Var} =
\frac{35}{12} + \frac{35}{12} = \frac{35}{6} \approx 5.83$.

## 6. The spread of the mean

**Question:** A measurement with standard deviation $10$ is repeated $25$
times independently. What is the standard deviation of the mean?

$\frac{10}{\sqrt{25}} = 2$.

## 7. A continuous variable

**Question:** On $[0, 1]$, $f(x) = 3x^2$. What are $P(X \leq 0.5)$, $E[X]$
and the variance?

$\int_0^{0.5} 3x^2 \, dx = 0.5^3 = 0.125$. $E[X] = \int_0^1 3x^3 \, dx =
\frac{3}{4}$. $E[X^2] = \frac{3}{5}$; variance $\frac{3}{5} - \frac{9}{16} =
\frac{3}{80}$.

## 8. The uniform distribution

**Question:** $X$ is uniform on $[0, 10]$. What are $P(2 \leq X \leq 5)$,
$E[X]$ and the variance?

The density is $\frac{1}{10}$: probability $\frac{3}{10}$. $E[X] = 5$,
variance $\frac{100}{12} \approx 8.33$.

## 9. Dropout

**Question:** The keep probability is $p = 0.5$ and a neuron's output is
$6$. What is the expected output during training?

Kept: $\frac{6}{0.5} = 12$; dropped: $0$. $0.5 \cdot 12 = 6$. The scale is
preserved.

## 10. The variance of a difference

**Question:** For independent $X$ and $Y$, $\operatorname{Var}(X) = 4$ and
$\operatorname{Var}(Y) = 9$. What is $\operatorname{Var}(X - Y)$?

$\operatorname{Var}(X) + (-1)^2 \operatorname{Var}(Y) = 13$. Subtracting
also increases the spread.
