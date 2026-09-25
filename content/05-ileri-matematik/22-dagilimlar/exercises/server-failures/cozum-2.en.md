**Idea:** No failure in $t$ hours means the number of failures in that time is $0$. The number of failures is Poisson$(\frac{t}{200})$.

**Step 1 — The mean.** $\frac{1}{200}$ failures per hour; on average $200$ hours between failures.

**Step 2 — $100$ hours.** The expected number of failures in $100$ hours is $0.5$; for a Poisson $P(0) = e^{-0.5} \approx 0.6065$.

**Step 3 — The median.** $P(0) = e^{-t/200} = \frac{1}{2}$, $t = 200 \ln 2$.

**Why the same result?** "The wait is longer than $t$" and "zero events in time $t$" are the same event; the exponential is the waiting time of a Poisson process.

**Answer:** $200$, $0.6065$ and $138.63$.
