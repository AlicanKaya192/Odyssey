**What is asked?** The amount left after a given time for a known half-life, the time to fall to a given amount, and the hourly decay factor.

**Idea:** The amount left is $N(t) = 240 \cdot \left( \frac{1}{2} \right)^{t / 4}$.

**Step 1 — $12$ hours.** $\frac{12}{4} = 3$ half-lives:

$$
N(12) = 240 \cdot \left( \tfrac{1}{2} \right)^3 = \frac{240}{8} = 30
$$

**Step 2 — $7.5$ mg.** $240 \cdot \left( \frac{1}{2} \right)^{t / 4} = 7.5$, so $2^{t / 4} = \frac{240}{7.5} = 32 = 2^5$. Equal exponents: $\frac{t}{4} = 5$, $t = 20$ hours.

**Step 3 — The hourly factor.** Over four hours the factor is $\frac{1}{2}$; if the hourly factor is $c$, then $c^4 = \frac{1}{2}$:

$$
c = \left( \tfrac{1}{2} \right)^{1/4} = \frac{1}{\sqrt[4]{2}} \approx 0.8409
$$

So it falls by about $15.9$ percent every hour.

**Check:** $0.8409^4 \approx 0.5$ ✓.

**Watch out:** The hourly decrease is not $12.5$ percent ($50 / 4$); percentages are not divided up, the factor is shared out by taking a root.

**Answer:** $30$ mg, $20$ hours, $0.8409$.
