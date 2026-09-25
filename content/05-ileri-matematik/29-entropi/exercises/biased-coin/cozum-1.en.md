**What is asked?** The entropy of a biased coin and the information of each outcome.

**Idea:** $H = -\sum p\log_2 p$; the information of one outcome is $-\log_2 p$.

**Step 1 — Entropy.** $0.9 \cdot 0.152 + 0.1 \cdot 3.322 \approx 0.137 + 0.332 = 0.469$ bits.

**Step 2 — Tails.** $-\log_2 0.1 \approx 3.322$ bits.

**Step 3 — Heads.** $-\log_2 0.9 \approx 0.152$ bits.

**Check:** Less than a fair coin's $1$ bit ✓; the rare outcome (tails) carries much more information than the frequent one ✓.

**Watch out:** The entropy is not the plain average of the two informations ($\frac{3.322 + 0.152}{2} = 1.737$); it is their probability-weighted average.

**Answer:** $\approx 0.469$, $\approx 3.322$, $\approx 0.152$.
