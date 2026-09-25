**Idea:** Work with the variance instead of the standard deviation; for an independent sum variances add.

**Step 1 — The variance.** One gradient has variance $16$. The sum of $64$ gradients has $64 \cdot 16$; multiplying by $\frac{1}{64}$ for the mean gives variance $\frac{64 \cdot 16}{64^2} = \frac{16}{64} = 0.25$; standard deviation $0.5$.

**Step 2 — The target.** A standard deviation of $0.25$ means variance $0.0625 = \frac{16}{n}$, $n = 256$.

**Step 3 — Dropout.** If the kept output is $v$, $0.8 v = 2$, $v = 2.5$.

**Why the same result?** $\operatorname{Var}(\frac{1}{n}\sum X_i) = \frac{1}{n^2} \cdot n\sigma^2 = \frac{\sigma^2}{n}$: that is where the $\frac{\sigma}{\sqrt{n}}$ rule comes from. The dropout question is an expected-value equation too.

**Answer:** $0.5$, $256$ and $2.5$.
