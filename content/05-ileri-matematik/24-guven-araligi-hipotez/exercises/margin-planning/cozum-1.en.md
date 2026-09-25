**What is asked?** The margin of error, and the sample size needed for a target margin.

**Idea:** $E = z^{*}\frac{\sigma}{\sqrt{n}}$; solved for $n$, $n = \left(\frac{z^{*}\sigma}{E}\right)^2$.

**Step 1 — $n = 100$.** $1.96 \cdot \frac{20}{10} = 3.92$.

**Step 2 — 95 percent.** $\left(\frac{1.96 \cdot 20}{2}\right)^2 = 19.6^2 = 384.16$; round up: $385$.

**Step 3 — 99 percent.** $\left(\frac{2.576 \cdot 20}{2}\right)^2 = 25.76^2 = 663.58$; round up: $664$.

**Check:** With $385$ observations the margin is $1.96 \cdot \frac{20}{\sqrt{385}} \approx 1.998 \leq 2$ ✓; with $384$ it is $\approx 2.0004$, slightly over.

**Watch out:** Rounding $384.16$ down to $384$ pushes the margin over the limit; when "at least" is asked, always round up.

**Answer:** $3.92$, $385$, $664$.
