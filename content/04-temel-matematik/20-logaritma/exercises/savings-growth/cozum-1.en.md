**What is asked?** The money grows by 8% each year; how many years until 1000 becomes 2500? The unknown number of years sits **in the exponent**, so we will need a logarithm.

**Idea:** Growing by 8% a year means being multiplied by $1.08$ every year. After $t$ years the money is $1000 \cdot 1.08^t$. The way to bring $t$ down from the exponent is to take the logarithm of both sides; the power rule ($\ln x^n = n \ln x$) moves the exponent to the front.

**Step 1 — Set up the equation.**

$$
1000 \cdot 1.08^t = 2500
$$

**Step 2 — Isolate the power.** Divide both sides by 1000:

$$
1.08^t = 2.5
$$

Meaning: the money has to grow $2.5$ times.

**Step 3 — Take the natural logarithm of both sides.** Equal numbers have equal logarithms. The power rule brings the exponent down in front:

$$
\begin{aligned}
\ln (1.08^t) &= \ln 2.5 \\
t \cdot \ln 1.08 &= \ln 2.5
\end{aligned}
$$

**Step 4 — Isolate $t$.** Divide both sides by $\ln 1.08$ and put in the given values:

$$
\begin{aligned}
t &= \frac{\ln 2.5}{\ln 1.08} \\
&\approx \frac{0.9163}{0.0770} \\
&\approx 11.90
\end{aligned}
$$

The rounded values given give $11.90$, more precise values give $11.91$; both are accepted.

**Check (does it make sense?):** In 11 years the money grows $1.08^{11} \approx 2.33$ times, in 12 years $1.08^{12} \approx 2.52$ times. $2.5$ times is between them and very close to 12. The result is sensible. ✓

**Answer:** about 11.91 years.
