**What is asked?** Individual and average log-loss, and the price of being sure and wrong.

**Idea:** For each example, minus the log of the probability given to the correct class.

**Step 1 — Third.** $y = 1$, $-\ln 0.4 \approx 0.916$.

**Step 2 — Average.** The first is $-\ln 0.9 \approx 0.105$; the second has $y = 0$, $-\ln 0.8 \approx 0.223$. Sum $1.245$; average $\approx 0.415$.

**Step 3 — $p_3 = 0.01$.** $-\ln 0.01 \approx 4.605$: on its own more than ten times the other two combined.

**Check:** The first example, which gives the correct class the highest probability ($0.9$), has the smallest loss ✓.

**Watch out:** Taking $-\ln 0.2$ for the second example; since $y = 0$, the correct class's probability is $1 - 0.2 = 0.8$.

**Answer:** $\approx 0.916$, $\approx 0.415$, $\approx 4.605$.
