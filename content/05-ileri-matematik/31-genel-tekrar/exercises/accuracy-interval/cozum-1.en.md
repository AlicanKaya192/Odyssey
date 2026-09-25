**What is asked?** The uncertainty of test accuracy.

**Idea:** Accuracy is a sample proportion; by the CLT it is approximately normal.

**Step 1 — SE.** $\hat{p} = 0.85$. $\sqrt{\frac{0.85 \cdot 0.15}{400}} = \sqrt{0.000319} \approx 0.0179$.

**Step 2 — Lower bound.** Margin of error $1.96 \cdot 0.0179 \approx 0.035$; $0.85 - 0.035 = 0.815$.

**Step 3 — Upper bound.** $0.885$.

**Check:** The interval is $0.07$ wide; with four times the $n$ it would halve ✓.

**Watch out:** Building the interval as $0.85 \pm 1.96 \cdot \sqrt{0.85 \cdot 0.15}$ gives the uncertainty of a single example; do not forget to divide by $n$.

**Answer:** $\approx 0.0179$, $\approx 0.815$, $\approx 0.885$.
