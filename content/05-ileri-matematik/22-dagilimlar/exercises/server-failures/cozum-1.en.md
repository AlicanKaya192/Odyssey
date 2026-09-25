**What is asked?** The mean, a tail probability and the median of an exponential waiting time.

**Idea:** $P(X > t) = e^{-\lambda t}$, $E[X] = \frac{1}{\lambda}$.

**Step 1 — The mean.** $\frac{1}{1/200} = 200$ hours.

**Step 2 — $100$ hours.** $e^{-100/200} = e^{-0.5} \approx 0.6065$.

**Step 3 — The median.** $e^{-t/200} = 0.5$, $-\frac{t}{200} = \ln 0.5 = -\ln 2$, $t = 200 \ln 2 \approx 138.63$ hours.

**Check:** The median is smaller than the mean ($138.63 < 200$): the exponential is right-skewed, long waits pull the mean up ✓.

**Watch out:** Thinking half the probability is used up by $200$ because "the mean is $200$ hours"; $P(X > 200) = e^{-1} \approx 0.37$.

**Answer:** $200$, $\approx 0.6065$, $\approx 138.63$.
