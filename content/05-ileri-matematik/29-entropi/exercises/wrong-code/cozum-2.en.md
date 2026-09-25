**Idea:** In the best code, A, B, C, D get lengths $1, 2, 3, 3$ bits (codes $0$, $10$, $110$, $111$). In the engineer's code they are all $2$ bits.

**Step 1 — Best code.** Average length $\frac{1}{2} \cdot 1 + \frac{1}{4} \cdot 2 + \frac{1}{4} \cdot 3 = 1.75$.

**Step 2 — Engineer's code.** Every state is $2$ bits; average $2$.

**Step 3 — Loss.** $0.25$ extra bits per outcome; $250{,}000$ bits over a million readings.

**Why the same result?** Since the probabilities are powers of $2$, the best code's lengths are exactly $-\log_2 p$; the assumed $Q$'s code lengths are $-\log_2 q$. The average lengths are exactly $H(P)$ and $H(P, Q)$.

**Answer:** $1.75$, $2$ and $0.25$.
