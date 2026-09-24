**Idea:** Estimate the quotient roughly, multiply your estimate by the divisor, then correct by looking at the difference. A practical way to avoid long division without a calculator.

**Step 1 — A rough estimate.** $2\,025 \approx 2\,000$ and $17 \approx 20$: the quotient is about $2\,000 \div 20 = 100$. But $17$ is less than $20$, so the quotient should be a bit more than $100$.

**Step 2 — A better guess: $120$.** $17 \cdot 120 = 2\,040$. That is **larger** than $2\,025$: $120$ is too many.

**Step 3 — One less: $119$.** $17 \cdot 119 = 2\,040 - 17 = 2\,023$. That is smaller than $2\,025$, with a difference of $2\,025 - 2\,023 = 2$.

**Step 4 — Check the remainder.** $2 < 17$: one more $17$ does not fit. Quotient $119$, remainder $2$.

**Why the same result?** The first method took off $17$s in chunks; this one started from an estimate and corrected it in one step. Both reach $2\,025 = 17 \cdot 119 + 2$, and this form is unique: since the remainder must be between $0$ and $16$, there is no other $(q, r)$ pair.

**Answer:** $119$ and $2$.
