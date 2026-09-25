**Idea:** For a node with $n$ examples and class counts $n_k$, $H = \log_2 n - \frac{1}{n}\sum n_k\log_2 n_k$. The split can be computed straight from the counts.

**Step 1 — Left.** $\log_2 6 - \frac{5\log_2 5 + 1 \cdot 0}{6} \approx 2.585 - \frac{11.610}{6} \approx 2.585 - 1.935 = 0.650$.

**Step 2 — Right and average.** $\log_2 10 - \frac{3\log_2 3 + 7\log_2 7}{10} \approx 3.322 - \frac{4.755 + 19.651}{10} \approx 3.322 - 2.441 = 0.881$. The weighted average is $\frac{6 \cdot 0.650 + 10 \cdot 0.881}{16} \approx 0.795$.

**Step 3 — Gain.** $1 - 0.795 \approx 0.205$.

**Why the same result?** $-\sum\frac{n_k}{n}\log_2\frac{n_k}{n} = -\sum\frac{n_k}{n}(\log_2 n_k - \log_2 n)$; expanding gives $\log_2 n - \frac{1}{n}\sum n_k\log_2 n_k$. Decision tree libraries work with counts in this form.

**Answer:** $0.650$, $0.795$ and $0.205$.
