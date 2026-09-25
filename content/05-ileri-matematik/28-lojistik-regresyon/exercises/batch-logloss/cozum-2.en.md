**Idea:** The total log-loss is minus the log of the product of the correct-class probabilities (the likelihood).

**Step 1 — Third.** The correct-class probability is $0.4$; $-\ln 0.4 \approx 0.916$.

**Step 2 — Product.** $L = 0.9 \cdot 0.8 \cdot 0.4 = 0.288$. $-\ln 0.288 \approx 1.245$; divided by $3$, $0.415$.

**Step 3 — $p_3 = 0.01$.** The likelihood drops to $0.9 \cdot 0.8 \cdot 0.01 = 0.0072$; the third example's share is $-\ln 0.01 \approx 4.605$.

**Why the same result?** $-\ln(abc) = -\ln a - \ln b - \ln c$; log-loss is exactly the likelihood split into sums. When a single probability approaches zero the whole product collapses; in logs this shows up as one term blowing up.

**Answer:** $0.916$, $0.415$ and $4.605$.
