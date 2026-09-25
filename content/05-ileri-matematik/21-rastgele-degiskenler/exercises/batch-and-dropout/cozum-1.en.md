**What is asked?** The noise of a mini-batch gradient and the scaling in dropout.

**Idea:** The standard deviation of the mean of $n$ independent observations is $\frac{\sigma}{\sqrt{n}}$; dropout preserves the expected output.

**Step 1 — $64$ examples.** $\frac{4}{\sqrt{64}} = \frac{4}{8} = 0.5$.

**Step 2 — Half of it.** $0.25 = \frac{4}{\sqrt{n}}$, $\sqrt{n} = 16$, $n = 256$.

**Step 3 — Dropout.** $\frac{2}{0.8} = 2.5$. The expected value is $0.8 \cdot 2.5 + 0.2 \cdot 0 = 2$ ✓.

**Check:** Halving the standard deviation takes four times as many examples ($64 \to 256$) ✓.

**Watch out:** Dividing the standard deviation by $n$ ($\frac{4}{64}$); $n$ divides the variance, the standard deviation by $\sqrt{n}$.

**Answer:** $0.5$, $256$, $2.5$.
