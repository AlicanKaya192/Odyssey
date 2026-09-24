**What is asked?** $3^{40}$ is a huge number. We find how many digits it has without computing it.

**Idea:** The number of digits depends on which two powers of 10 the number sits between:

- Numbers from $10^1 = 10$ up to $10^2 = 100$ have 2 digits.
- Numbers from $10^2 = 100$ up to $10^3 = 1000$ have 3 digits.

In general, if $10^k \le N < 10^{k+1}$, then $N$ has $k + 1$ digits. And $\log_{10}$ tells us between which powers of 10 a number lies.

**Step 1 — Compute the logarithm with the power rule.** Power rule: $\log_b x^n = n \cdot \log_b x$ (the exponent comes down in front).

$$
\begin{aligned}
\log_{10} 3^{40} &= 40 \cdot \log_{10} 3 \\
&\approx 40 \cdot 0.4771 \\
&= 19.084
\end{aligned}
$$

**Step 2 — What this number means.** $\log_{10} 3^{40} \approx 19.084$ means $3^{40} \approx 10^{19.084}$. Since $19.084$ is between 19 and 20:

$$
10^{19} \le 3^{40} < 10^{20}
$$

**Step 3 — Read off the digits.** $10^{19}$ is a one followed by 19 zeros, the **smallest 20-digit number**. $10^{20}$ is the smallest 21-digit number. $3^{40}$ is between them, so it has 20 digits.

As a formula: the whole part of the logarithm plus 1.

$$
\lfloor 19.084 \rfloor + 1 = 19 + 1 = 20
$$

**Check:** Indeed $3^{40} = 12\,157\,665\,459\,056\,928\,801$; count them and you get 20 digits.

**Watch out:** The most common answer is 19. The whole part of the logarithm is **one less** than the number of digits; do not forget the $+1$. ($10 = 10^1$ has two digits, and its logarithm is 1.)

**Answer:** 20.
