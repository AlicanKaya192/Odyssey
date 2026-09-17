**1. Compute the logarithm with the power rule:**

$$
\log_{10} 3^{40} = 40 \cdot \log_{10} 3 \approx 40 \cdot 0.4771 = 19.084
$$

**2. What does this mean?** The logarithm is between 19 and 20, so

$$
10^{19} \le 3^{40} < 10^{20}
$$

$10^{19}$ is a one followed by 19 zeros, the smallest number with **20 digits**. $10^{20}$ is the smallest number with 21 digits. $3^{40}$ lies between them, so it has 20 digits.

**3. The formula gives the same result:**

$$
\lfloor 19.084 \rfloor + 1 = 19 + 1 = 20
$$

(Indeed $3^{40} = 12{,}157{,}665{,}459{,}056{,}928{,}801$, 20 digits.)

**Common mistake:** answering 19. The whole part of the logarithm is **one less** than the number of digits; do not forget the $+1$.

**Answer: 20**
