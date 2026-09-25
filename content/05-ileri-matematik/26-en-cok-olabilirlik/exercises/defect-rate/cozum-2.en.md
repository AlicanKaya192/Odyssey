**Idea:** For $k$ successes in $n$ observations $\hat{p} = \frac{k}{n}$; $\ell(\hat{p}) = n\big[\hat{p}\ln\hat{p} + (1 - \hat{p})\ln(1 - \hat{p})\big]$ and $\ell'(p) = \frac{n(\hat{p} - p)}{p(1 - p)}$.

**Step 1 — MLE.** $\frac{8}{200} = 0.04$.

**Step 2 — $\ell(\hat{p})$.** $200 \cdot \big[0.04 \cdot (-3.2189) + 0.96 \cdot (-0.0408)\big] = 200 \cdot (-0.1679) \approx -33.59$.

**Step 3 — $\ell'(0.05)$.** $\frac{200 \cdot (0.04 - 0.05)}{0.05 \cdot 0.95} = \frac{-2}{0.0475} \approx -42.11$.

**Why the same result?** Over a common denominator $\frac{k}{p} - \frac{n - k}{1 - p}$ becomes $\frac{k - np}{p(1 - p)}$, and $k = n\hat{p}$; the second formula is the first simplified. The expression in brackets is minus the entropy we will meet in the Entropy section.

**Answer:** $0.04$, $-33.59$ and $-42.11$.
