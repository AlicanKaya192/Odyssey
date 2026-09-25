**What is asked?** The value of an exponentially growing number at a given time, its doubling time, and when it passes a threshold.

**Idea:** Growth by the same rate each month is exponential: $N(t) = 2000 \cdot 1.1^t$. When the unknown is in the exponent, take a logarithm.

**Step 1 — $6$ months.** $1.1^6 \approx 1.771561$; $N(6) \approx 3543.12$.

**Step 2 — Doubling.** $1.1^t = 2$:

$$
t = \frac{\ln 2}{\ln 1.1} \approx \frac{0.69315}{0.09531} \approx 7.27
$$

**Step 3 — $10{,}000$.** $1.1^t = 5$, $t = \frac{\ln 5}{\ln 1.1} \approx 16.89$. The threshold is crossed during a month; looking at month ends, $\approx 9190$ at the end of month $16$ and $\approx 10{,}109$ at the end of month $17$. The first time is the end of month $17$.

**Check:** The rule of 72: at $10$ percent, doubling in about $\frac{72}{10} = 7.2$ months ✓.

**Watch out:** Computing $60$ percent over six months ($3200$ users) is simple interest; each month's growth comes on top of the grown number.

**Answer:** $\approx 3543.12$, $\approx 7.27$ months, month $17$.
