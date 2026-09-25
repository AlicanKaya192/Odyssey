**Idea:** $v$ is a weighted sum of past gradients: $v_{k+1} = g_k + \beta g_{k-1} + \beta^2 g_{k-2} + \cdots$. Use it to write each step directly.

**Step 1 — First.** $g_0 = 2$: $v_1 = 2$, $w_1 = 1 - 0.2 = 0.8$.

**Step 2 — Second.** $g_1 = 1.6$: $v_2 = 1.6 + 0.9 \cdot 2 = 3.4$, $w_2 = 0.8 - 0.34 = 0.46$.

**Step 3 — Third.** $g_2 = 0.92$: $v_3 = 0.92 + 0.9 \cdot 1.6 + 0.81 \cdot 2 = 0.92 + 1.44 + 1.62 = 3.98$, $w_3 = 0.46 - 0.398 = 0.062$.

**Step 4 — Plain descent.** $1 \cdot 0.8^3 = 0.512$.

**Why the same result?** The explicit sum is the recursive rule $v \leftarrow \beta v + g$ unrolled step by step. The unrolling also shows why it speeds up: as long as the gradients keep the same sign, their contributions pile up; in a consistent direction the effective step size can grow to about $\frac{\eta}{1 - \beta} = 1$, ten times as much.

**Answer:** $0.46$, $0.062$, $0.512$.
