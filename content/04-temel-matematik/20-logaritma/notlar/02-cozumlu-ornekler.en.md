A worked example, step by step, for each method in the lesson. Try to solve the question yourself first, then read the solution.

## 1. A logarithm through a common base

**Question:** What is $\log_4 8$?

8 is not a whole power of 4. But both are powers of 2: $4 = 2^2$, $8 = 2^3$.

If $\log_4 8 = y$ then $4^y = 8$:

$$
(2^2)^y = 2^3
\quad\Rightarrow\quad
2^{2y} = 2^3
\quad\Rightarrow\quad
2y = 3
\quad\Rightarrow\quad
y = \frac{3}{2}
$$

**Check:** $4^{3/2} = (\sqrt{4})^3 = 2^3 = 8$. ✓

With the same method $\log_9 3 = \frac{1}{2}$ ($9^{1/2} = 3$) and
$\log_8 2 = \frac{1}{3}$ ($8^{1/3} = 2$).

## 2. Simplifying with several rules together

**Question:** What is $2 \log_3 6 - \log_3 4$?

**1. Move the coefficient inside with the power rule:**

$$
2 \log_3 6 = \log_3 6^2 = \log_3 36
$$

**2. Combine the difference with the quotient rule:**

$$
\log_3 36 - \log_3 4 = \log_3 \frac{36}{4} = \log_3 9
$$

**3.** $3^2 = 9$, so the answer is $2$.

Order matters: **move coefficients inside first, then combine.** A common
mistake is applying the 2 to the whole expression:
$2 (\log_3 6 - \log_3 4) = 2 \log_3 1.5 \approx 0.74$ is a completely
different number. In the expression, the 2 is the coefficient of the first
term only.

## 3. No logarithm needed when the bases match

**Question:** $2^{3x - 1} = 32$

Write 32 as a power of 2: $32 = 2^5$.

$$
2^{3x - 1} = 2^5
\quad\Rightarrow\quad
3x - 1 = 5
\quad\Rightarrow\quad
x = 2
$$

Because the exponential function is one-to-one, equal bases mean equal
exponents. Taking logarithms gives the same result but is unnecessary work.

## 4. An exponential equation with a coefficient

**Question:** $5 \cdot 3^x = 25$

**1. Isolate the power term:** $3^x = 5$.

5 is not a whole power of 3; a logarithm is needed.

**2. Take the logarithm and bring the exponent down:**

$$
x \ln 3 = \ln 5
\quad\Rightarrow\quad
x = \frac{\ln 5}{\ln 3} \approx \frac{1.609}{1.099} \approx 1.465
$$

**Sanity check:** $3^1 = 3$ and $3^2 = 9$; 5 lies between them, and $x$ lies
between 1 and 2. ✓

## 5. A growth problem

**Question:** A community of 200 people grows by 10% every year. After how
many years does it reach 1000 people?

$$
200 \cdot 1.1^t = 1000
\quad\Rightarrow\quad
1.1^t = 5
\quad\Rightarrow\quad
t = \frac{\ln 5}{\ln 1.1} \approx \frac{1.609}{0.0953} \approx 16.89
$$

About 17 years. Every growth problem follows this pattern:
**start · (1 + rate)ᵗ = target.** For shrinking quantities the rate has a
minus sign ($0.8$ for a 20% decrease).

## 6. A logarithmic equation and the check

**Question:** $\log_3 x + \log_3 (x - 8) = 2$

**1. Combine:** $\log_3 \big(x(x - 8)\big) = 2$

**2. Rewrite with the definition:** $x(x - 8) = 3^2 = 9$

**3. Solve:** $x^2 - 8x - 9 = 0$, so $(x - 9)(x + 1) = 0$. Candidates: $9$ and $-1$.

**4. Check:**

- $x = 9$: $\log_3 9 + \log_3 1 = 2 + 0 = 2$. ✓
- $x = -1$: $\log_3 (-1)$ is undefined. ✕

**Answer: $x = 9$.**

## 7. Estimating without a calculator

**Question:** What is $\log_{10} 3000$ approximately? ($\log_{10} 3 \approx 0.477$)

Write the number as "a number times a power of 10":

$$
\log_{10} 3000 = \log_{10} (3 \cdot 10^3) = \log_{10} 3 + 3 \approx 3.477
$$

The whole part (3) is one less than the number of digits; the decimal part
(0.477) comes from the leading digits. The logarithms of 3000, 30,000 and
300,000 share the same decimal part: $3.477$, $4.477$, $5.477$.
