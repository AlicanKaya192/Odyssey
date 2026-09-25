**What is asked?** The number and probability of false alarms when many tests are run.

**Idea:** When $H_0$ holds, each test rejects with probability $\alpha$; for independent tests the probabilities multiply.

**Step 1 — Expected number.** $20 \cdot 0.05 = 1$.

**Step 2 — At least one.** None of them giving a false alarm has probability $0.95^{20} \approx 0.358$; the complement is $1 - 0.358 = 0.642$.

**Step 3 — Bonferroni.** $\frac{0.05}{20} = 0.0025$.

**Check:** With the corrected threshold the probability of at least one false alarm is $1 - 0.9975^{20} \approx 0.049 \leq 0.05$ ✓.

**Watch out:** Reporting "the one setting that came out significant" is often reporting this false alarm; how many things were tried must be said too.

**Answer:** $1$, $\approx 0.642$, $0.0025$.
