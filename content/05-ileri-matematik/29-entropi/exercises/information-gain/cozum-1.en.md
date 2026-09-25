**What is asked?** How much a decision tree split lowers the entropy.

**Idea:** Gain $= H(\text{parent}) - \left[\frac{6}{16}H(\text{left}) + \frac{10}{16}H(\text{right})\right]$.

**Step 1 — Left.** $-\log_2\frac{5}{6} = \log_2 6 - \log_2 5 \approx 0.263$; $-\log_2\frac{1}{6} \approx 2.585$. $H \approx \frac{5}{6} \cdot 0.263 + \frac{1}{6} \cdot 2.585 \approx 0.219 + 0.431 = 0.650$.

**Step 2 — Right and average.** $-\log_2 0.3 = \log_2 10 - \log_2 3 \approx 1.737$; $-\log_2 0.7 \approx 0.515$. $H \approx 0.3 \cdot 1.737 + 0.7 \cdot 0.515 \approx 0.881$. Weighted: $0.375 \cdot 0.650 + 0.625 \cdot 0.881 \approx 0.795$.

**Step 3 — Gain.** $1 - 0.795 = 0.205$ bits.

**Check:** The gain lies between $0$ and $1$ ✓; both children are purer than the parent ✓.

**Watch out:** Averaging the children's entropies without weights ($\frac{0.650 + 0.881}{2} = 0.766$) understates the effect of the larger group.

**Answer:** $\approx 0.650$, $\approx 0.795$, $\approx 0.205$.
